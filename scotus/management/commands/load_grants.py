import datetime

from clerk import scdb, scores, scotus
from dateutil import parser
from django.core.management.base import BaseCommand, CommandError

from clerk import utils as clerk_utils
from docket import grants
from scotus import models

class Command(BaseCommand):

    def load_grants(self):
        s = grants.Load(terms=[int(clerk_utils.current_term())])
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
            obj, created = models.MeritsCase.objects.update_or_create(docket=case.docket,term=case.term,defaults=case.__dict__)
            print created, obj

    def handle(self, *args, **kwargs):
        self.load_grants()