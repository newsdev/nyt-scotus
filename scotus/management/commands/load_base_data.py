import datetime

from clerk import scdb, scores, scotus
from dateutil import parser
from django.core.management.base import BaseCommand, CommandError

from scotus import models

class Command(BaseCommand):

    def load_scdb_data(self):
        """
        Loads case / justice data from SCDB's
        justice-centered file which contains
        a single row for every justice-vote on
        an individual case.
        """
        s = scdb.Load()
        s.clean()
        s.download()
        s.load()

        # Cases come across from nyt-clerk with date strings.
        # Parse these to datetime objects.
        cases = []
        for case in s.cases:
            for k,v in case.__dict__.items():
                if 'date' in k:
                    setattr(case,k,parser.parse(v))
            cases.append(models.MeritsCase(**case.__dict__))

        # Bulk creation of objects works here.
        # Later, we'll have to do update_or_create.
        models.MeritsCase.objects.bulk_create(cases, 500)

        # Creating justices 
        justices = [models.Justice(**justice.__dict__) for justice in s.justices]
        models.Justice.objects.bulk_create(justices, 500)

        votes = []
        for vote in s.votes:
            for k,v in vote.__dict__.items():
                if 'date' in k:
                    setattr(vote,k,parser.parse(v))
            votes.append(models.Vote(**vote.__dict__))
        models.Vote.objects.bulk_create(votes, 500)

        naturalcourts = []
        for naturalcourt in s.naturalcourts:
            for k,v in naturalcourt.__dict__.items():
                if 'date' in k:
                    if v:
                        setattr(naturalcourt,k,parser.parse(v))
            naturalcourts.append(models.NaturalCourt(**naturalcourt.__dict__))
        models.NaturalCourt.objects.bulk_create(naturalcourts, 500)

        s.clean()

    def load_scores_data(self):
        """
        Loads Martin-Quinn scores for terms / justices and
        Segal-Cover scores for justices from CSVs.
        """
        s = scores.Load()
        s.clean()
        s.download()
        s.load()

        # Need to update the Justice objects that already exist.
        # Also layers on last name to votes for ease of use.
        for justice in s.justices:
            models.Justice.objects.filter(justice=justice.justice).update(**justice.__dict__)
            models.Vote.objects.filter(justice=justice.justice).update(last_name=justice.last_name)

        courtterms = [models.CourtTerm(**courtterm.__dict__) for courtterm in s.courtterms]
        models.CourtTerm.objects.bulk_create(courtterms, 500)

        justiceterms = [models.JusticeTerm(**justiceterm.__dict__) for justiceterm in s.justiceterms]
        models.JusticeTerm.objects.bulk_create(justiceterms, 500)

        s.clean()

    def load_scotus_data(self):
        """
        Loads opinions and argument audio / transcripts
        from SupremeCourt.gov. Also gets a nicer case
        name. Data only really available for the 2000s.
        """
        s = scotus.Load()
        s.scrape_opinions()
        s.scrape_audio()
        s.scrape_arguments()
        s.parse_opinions()
        s.parse_audio()
        s.parse_arguments()

        for case in [v for k,v in s.cases.items()]:
            for k,v in case.items():
                if 'date' in k:
                    case[k] = parser.parse(v)

            models.MeritsCase.valid_cases\
                .filter(docket=case['docket'], term=case['term'])\
                .update(**case)

    def handle(self, *args, **options):
        """
        Loads SCDB cases (critical these are first) and then
        MQ / SC scores and finally data from SupremeCourt.gov.
        """
        start = datetime.datetime.now()
        print "Loading SCDB data."
        self.load_scdb_data()
        print "Loading scores."
        self.load_scores_data()
        print "Loading SCOTUS data."
        self.load_scotus_data()

        end = datetime.datetime.now()

        print "Took %s" % (end - start)