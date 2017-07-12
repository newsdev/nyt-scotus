import sys

from django.core.management.base import BaseCommand
from django.conf import settings
import ujson as json

from scotus.models import Vote

class Command(BaseCommand):

    def handle(self, *args, **options):
        payload = {}
        for j in settings.ACTIVE_JUSTICES:
            payload[j['justicename']] = {
                "terms": {},
                "all-time": {
                    9: {"majority": 0, "dissent": 0},
                    8: {"majority": 0, "dissent": 0},
                    7: {"majority": 0, "dissent": 0},
                    6: {"majority": 0, "dissent": 0},
                    5: {"majority": 0, "dissent": 0},
                    4: {"majority": 0, "dissent": 0},
                }
            }
            votes = [(v['majvotes'], v['majority'], v['term']) for v in Vote.valid.filter(justice=j['justice']).values('majvotes', 'majority', 'term')]
            for majvotes, majority, term in votes:
                if not payload[j['justicename']]['terms'].get(term, None):
                    payload[j['justicename']]['terms'][term] = {
                        9: {"majority": 0, "dissent": 0},
                        8: {"majority": 0, "dissent": 0},
                        7: {"majority": 0, "dissent": 0},
                        6: {"majority": 0, "dissent": 0},
                        5: {"majority": 0, "dissent": 0},
                        4: {"majority": 0, "dissent": 0},
                    }


                # From http://scdb.wustl.edu/documentation.php?var=majority
                # "1" means dissent, "2" means majority
                if majority == "2":
                    payload[j['justicename']]['all-time'][majvotes]['majority'] += 1
                    payload[j['justicename']]['terms'][term][majvotes]['majority'] += 1
                if majority == "1":
                    payload[j['justicename']]['all-time'][majvotes]['dissent'] += 1
                    payload[j['justicename']]['terms'][term][majvotes]['dissent'] += 1

        sys.stdout.write(json.dumps(payload))
