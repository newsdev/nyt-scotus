import datetime

from clerk import scdb, scores, scotus
from dateutil import parser
from django.core.management.base import BaseCommand, CommandError

from clerk import utils as clerk_utils
from docket import grants
from scotus import models

class Command(BaseCommand):

    def load_grants(self):
        s = grants.Load()
        s.scrape()

        for case in s.cases:
            for k,v in case.__dict__.items():
                if 'date' in k:
                    if v:
                        try:
                            v = v.strip().split()[0].strip()
                            setattr(case,k,parser.parse(v))
                        except ValueError:
                            print v

            try:
                c = models.MeritsCase.objects.get(docket=case.docket,term=case.term)
                for k,v in case.__dict__.items():
                    if not getattr(c,k, None):
                        setattr(c,k,v)
                c.save()
                print "^ %s" % c.casename
            except models.MeritsCase.DoesNotExist:
                c = models.MeritsCase(**case.__dict__)
                c.save()
                print "+ %s" % c.casename

            except models.MeritsCase.MultipleObjectsReturned:
                c = models.MeritsCase.objects.filter(docket=case.docket,term=case.term,casename=case.casename)
                if c.count() == 1:
                    c = c[0]
                    for k,v in case.__dict__.items():
                        if not getattr(c,k, None):
                            setattr(c,k,v)
                    c.save()
                    print "^ %s" % c.casename
                else:
                    print "Duplicate cases: " + ", ".join([z.id for z in c])

    def handle(self, *args, **kwargs):
        self.load_grants()