from django.core.management.base import BaseCommand, CommandError

from clerk import scdb, scores, scotus
from dateutil import parser
from scotus import models

class Command(BaseCommand):

    def load_scdb_data(self):
        s = scdb.Load()
        s.clean()
        s.download()
        s.load()

        for case in s.cases:
            case_dict = dict(case.__dict__)
            for k,v in case_dict.items():
                if 'date' in k:
                    case_dict[k] = parser.parse(v)

            obj, created = models\
                            .MeritsCase\
                            .objects\
                            .update_or_create(caseid=case.caseid,defaults=case_dict)
            print obj, created

        for justice in s.justices:
            obj, created = models\
                            .Justice\
                            .objects\
                            .update_or_create(justice=justice.justice,defaults=justice.__dict__)
            print obj, created

        for vote in s.votes:
            obj, created = models\
                            .Vote\
                            .objects\
                            .update_or_create(caseid=vote.caseid,justice=vote.justice,defaults=vote.__dict__)
            print obj, created

        s.clean()

    def load_scores_data(self):
        s = scores.Load()
        s.download()
        s.load()

        for justice in s.justices:
            obj, created = models\
                            .Justice\
                            .objects\
                            .update_or_create(justice=justice.justice,defaults=justice.__dict__)
            print obj, created

        for term in s.courtterms:
            obj, created = models\
                            .CourtTerm\
                            .objects\
                            .update_or_create(term=term.term,defaults=term.__dict__)
            print obj,created

        for term in s.justiceterms:
            obj, created = models\
                            .JusticeTerm\
                            .objects\
                            .update_or_create(term=term.term,justice=term.justice,defaults=term.__dict__)
            print obj, created

        s.clean()

    def load_scotus_data(self):
        s = scotus.Load()
        # s.scrape_opinions()
        # s.scrape_audio()
        s.scrape_arguments()
        # s.parse_opinions()
        # s.parse_audio()
        s.parse_arguments()

        for case in [v for k,v in s.cases.items()]:
            case_dict = dict(case)
            for k,v in case_dict.items():
                if 'date' in k:
                    case_dict[k] = parser.parse(v)

            print "%s\t%s\t%s" % (case_dict['term'], case_dict['docket'], case_dict['argument_pdf'])
            for m in models.MeritsCase.valid_cases.filter(docket=case_dict['docket'], term=case_dict['term']):
                for k,v in case_dict.items():
                    setattr(m,k,v)
                    m.save()

    def handle(self, *args, **options):
        # self.load_scdb_data()
        # self.load_scores_data()
        self.load_scotus_data()

