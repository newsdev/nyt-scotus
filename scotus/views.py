import csv
import glob
import json
import random

from bs4 import BeautifulSoup
from django.views.generic import ListView, DetailView
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.conf import settings
from django.db.models import Sum, Count
import ftfy
from lxml import etree

from clerk import utils as clerk_utils
from scotus import models
from scotus import utils

def filter_and_sum_api(request):
    params = dict(request.GET)

    grouper = 'term'
    order_by = '-term'
    values = ['id', 'name', 'majvotes', 'nyt_weighted_majvotes', 'term']

    if params.get('grouper', None):
        grouper = params['grouper'][-1]
        del params['grouper']

    if params.get('order_by', None):
        order_by = params['order_by'][-1]
        del params['order_by']

    if params.get('values', None):
        values = params['values'][-1].split(',')
        del params['values']

    query = models.MeritsCase.valid_objects.filter(decisiondirection__in=[u'2', u'1'])
    for k,v in params.items():
        kw = {}
        if "__in" in k:
            kw[k] = v[-1].split(',')
        else:
            kw[k] = v[-1]
        query = query.filter(**kw)
    query = query.order_by(order_by)
    query = query.values(*values)

    payload = {}
    for case in query:
        if not payload.get(case[grouper], None):
            payload[case[grouper]] = {}
            payload[case[grouper]]['cases'] = []
            payload[case[grouper]]['total'] = 0
        payload[case[grouper]]['cases'].append(case)
        payload[case[grouper]]['total'] += 1

    return HttpResponse(json.dumps(payload))

def voting_clusters(request, last_name):
    """
    naturalcourt is an SCDB natural court ID of a natural court, ex 1704 for Roberts 5.
    justices is a comma-separated string of Justice last_names, ex, kagan,alito.
    maxvotes is a comma-separated string of majority votes, ex, 5,6 gets all 5-4 and 6-3 decisions.
    term is a year representing the term, ex, 2014.
    /api/v1/voting/justice/Scalia/?term=2014&justices=Thomas,Roberts,Alito&maxvotes=5,6
    """
    j = models.Justice.objects.get(last_name=last_name)
    if request.GET.get('justices', None):
        justices = request.GET.get('justices', None).split(',')
        maxvotes = request.GET.get('maxvotes', None)
        term = request.GET.get('term', None)
        cc = j.common_cases(justices, naturalcourt=request.GET.get('naturalcourt', None), maxvotes=maxvotes, term=term)
        agree = j.agree_positions(justices, cc)
        disagree = j.disagree_positions(justices, cc)

        payload = {}
        payload['justice'] = j.get_name()
        payload['agree_number'] = agree[0]
        payload['agree_cases'] = []
        payload['disagree_number'] = disagree[0]
        payload['disagree_cases'] = []
        payload['common_cases_number'] = len(cc)
        payload['pct'] = float(agree[0] + disagree[0]) / len(cc)

        for pk in agree[1]:
            case_dict = {}
            c = models.MeritsCase.objects.get(caseid=pk)
            case_dict['casename'] = c.casename
            case_dict['term'] = c.term
            case_dict['spit'] = c.votes()
            payload['agree_cases'].append(case_dict)

        for pk in disagree[1]:
            case_dict = {}
            c = models.MeritsCase.objects.get(caseid=pk)
            case_dict['casename'] = c.casename
            case_dict['term'] = c.term
            case_dict['spit'] = c.votes()
            payload['disagree_cases'].append(case_dict)

        payload = json.dumps(payload)
        return HttpResponse(payload)

    return HttpResponse('400 bad request')

def cases_by_term(request):
    """
    /api/v1/case/by-term/
    Returns cases and their ideology grouped by Term.
    For a graphic by Alicia Parlapiano.
    term,share 9,share 8,share 7,share 6,share 5,share 0,share -5,share -6,share -7,share -8,share -9b,barwidth
    barwidth: number of terms
    term: term year
    """
    payload = []

    cases = models.MeritsCase.valid_objects.filter(decisiondirection__in=[u'2', u'1'])
    terms = range(1946, int(clerk_utils.current_term()) + 1)

    SHARE_KEYS = ("share -9","share -8","share -7","share -6","share -5","share 5","share 6","share 7","share 8","share 9")

    def init_court_row():
        payload = {}
        for key in SHARE_KEYS:
            payload[key] = 0
        payload['term'] = None
        payload['kennedy share -5'] = 0
        payload['kennedy share 5'] = 0
        payload['powell share -5'] = 0
        payload['powell share 5'] = 0
        return dict(payload)

    def compute_shares(row, case_count):
        if case_count > 0:
            for key in SHARE_KEYS:
                row[key] = float(row[key]) / float(case_count)
        return row

    def produce_row(row, header):
        """
        You can put the fields wherever you want.
        If the fields are not returned here, they will not be in the output.
        """
        output = (row['term'],)
        for key in SHARE_KEYS:
            output = output + (row[key],)
        output = output + (row["kennedy share -5"], row["kennedy share 5"], row["powell share -5"], row["powell share 5"])
        return output

    k = models.Justice.objects.get(last_name="Kennedy")
    p = models.Justice.objects.get(last_name="Powell")

    for term in terms:
        court_cases = models.MeritsCase.valid_objects.filter(decisiondirection__in=[u'2', u'1']).filter(term=term).values('casename', 'nyt_weighted_majvotes', 'term', 'decisiondirection')
        court_row = dict(init_court_row())
        court_row['term'] = term
        for c in court_cases:
            if c['nyt_weighted_majvotes']:
                court_row['share %s' % c['nyt_weighted_majvotes']] += 1
        court_row = compute_shares(court_row, court_cases.count())

        """
        Grab votes by kennedy and powell where they were on the winning side of a 5-4.
        """
        try:
            court_row['powell share -5'] = float(models.Vote.valid_objects.filter(justice=p.justice, term=term, nyt_weighted_majvotes=-5, majority="2", decisiondirection__in=[u'2', u'1']).count()) / court_cases.count()
            court_row['powell share 5'] = float(models.Vote.valid_objects.filter(justice=p.justice, term=term, nyt_weighted_majvotes=5, majority="2", decisiondirection__in=[u'2', u'1']).count()) / court_cases.count()
        except ZeroDivisionError:
            pass

        try:
            court_row['kennedy share -5'] = float(models.Vote.valid_objects.filter(justice=k.justice, term=term, nyt_weighted_majvotes=-5, majority="2", decisiondirection__in=[u'2', u'1']).count()) / court_cases.count()
            court_row['kennedy share 5'] = float(models.Vote.valid_objects.filter(justice=k.justice, term=term, nyt_weighted_majvotes=5, majority="2", decisiondirection__in=[u'2', u'1']).count()) / court_cases.count()
        except ZeroDivisionError:
            pass

        payload.append(court_row)

    payload = sorted(payload, key=lambda x:(x['term']))

    # return HttpResponse(json.dumps(payload))

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    header = ("term", "share -9","share -8","share -7","share -6","share -5","share 5","share 6","share 7","share 8","share 9", "kennedy share -5", "kennedy share 5", "powell share -5", "powell share 5")
    writer.writerow(header)
    for row in payload:
        writer.writerow(produce_row(row, header))
    return response


def cases_by_court(request):
    """
    /api/v1/case/by-court/
    Returns cases and their ideology grouped by NaturalCourt.
    For a graphic by Alicia Parlapiano.
    term,share 9,share 8,share 7,share 6,share 5,share 0,share -5,share -6,share -7,share -8,share -9,barwidth
    barwidth: number of natural courts
    term: natural court name
    """
    payload = []

    cases = models.MeritsCase.valid_objects.filter(decisiondirection__in=[u'2', u'1'])

    # Limit to the Vinson 1 court, 1946 to present.
    courts = [(c.naturalcourt, c.common_name, c.get_date_display()) for c in models.NaturalCourt.objects.filter(naturalcourt__gte=79)]

    SHARE_KEYS = ("share -9","share -8","share -7","share -6","share -5","share 5","share 6","share 7","share 8","share 9")

    def init_court_row():
        payload = {}
        for key in SHARE_KEYS:
            payload[key] = 0
        payload['term'] = None
        payload['barwidth'] = len(courts)
        return dict(payload)

    def compute_shares(row, case_count):
        if case_count > 0:
            for key in SHARE_KEYS:
                row[key] = float(row[key]) / float(case_count)
        return row

    def produce_row(row, header):
        output = (row['term'],)
        for key in SHARE_KEYS:
            output = output + (row[key],)
        return output

    for naturalcourt,name,dates in courts:
        court_cases = models.MeritsCase.valid_objects.filter(decisiondirection__in=[u'2', u'1']).filter(naturalcourt=naturalcourt).values('casename', 'nyt_weighted_majvotes', 'term', 'decisiondirection')
        court_row = dict(init_court_row())
        court_row['term'] = name
        court_row['start_date'] = dates.split(' - ')[0].strip()
        for c in court_cases:
            if c['nyt_weighted_majvotes']:
                court_row['share %s' % c['nyt_weighted_majvotes']] += 1
        court_row = compute_shares(court_row, court_cases.count())
        payload.append(court_row)

    payload = sorted(payload, key=lambda x:(x['start_date']))

    # return HttpResponse(json.dumps(payload))

    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)
    header = ("term", "share -9","share -8","share -7","share -6","share -5","share 5","share 6","share 7","share 8","share 9","barwidth")
    writer.writerow(header)
    for row in payload:
        writer.writerow(produce_row(row, header))
    return response
