import json

from django.core import serializers
from django.db import models
import ftfy
import smartypants


class ValidCasesManager(models.Manager):
    """
    Removes:
    1. Cases with split decisions (docketid ends with -02).
    2. Cases with split issues (caseissuesid ends with -02 ).
    3. All per curiams, decrees, divided votes and seriatim decisions.
    4. Inactive.
    Per Lee Epstein and Adam Liptak. Use this manager for doing
    any aggregations or sums of justice votes or court votes.
    """
    def get_queryset(self):
        return super(ValidCasesManager, self).get_queryset()\
            .filter(decisiontype__in=["1", "7"])\
            .filter(docketid__endswith="-01")\
            .filter(caseissuesid__endswith="-01")\


class BaseScotusModel(models.Model):

    class Meta:
        abstract = True

    def smart_dict(self):
        payload = self.dict()
        for key,value in payload.items():
            if value:
                try:
                    payload[key] = smartypants.smartypants(value.strip())
                except TypeError:
                    pass
                except UnicodeError:
                    pass
                except AttributeError:
                    pass
        return payload

    def dict(self):
        serialized = serializers.serialize('json', [self])
        payload = dict(json.loads(serialized)[0]['fields'])
        payload[u'pk'] = json.loads(serialized)[0]['pk']
        for key,value in payload.items():
            if value:
                try:
                    payload[key] = ftfy.fix_text(value.strip())
                except TypeError:
                    pass
                except UnicodeError:
                    pass
                except AttributeError:
                    pass
        return payload

    def json(self):
        return json.dumps(self.dict())


def webfix_unicode(possible_string):
    """
    This is ugly but it will create Times-approved HTML
    out of terrible cut-and-paste from decision text.
    """
    CHAR_MAP = [
        (u'\xa7', u'&sect;'),
        (u'\u2014', u'&mdash;'),
        (u'\u2013', u'&ndash;'),
        (u'\x97', u'&mdash;'),
        (u'\xa4', u'&euro;'),
        (u'\u201c', u'"'),
        (u'\u201d', u'"'),
        (u'\x96', u'&#150;'),
    ]

    if isinstance(possible_string, basestring):
        string = possible_string
        string = string.strip()
        for char, replace_char in CHAR_MAP:
            string = string.replace(char, replace_char)
        string = string.decode('utf-8')
        string = unicode(string)
        string = ftfy.fix_text(string)
        string = smartypants.smartypants(string)
        return string

    return possible_string
