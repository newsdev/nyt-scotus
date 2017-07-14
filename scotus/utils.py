import datetime

from django.template.context_processors import csrf
from django.core import serializers
from django.db import models
import ftfy
import smartypants
import ujson as json

def current_term():
    """
    Utility method for deciding the current term from today's date.
    """
    now = datetime.datetime.now()
    if now.month < 10:
        return "%s" % (now.year - 1)
    else:
        return "%s" % now.year


def make_context(request):
    """
    Utility method for adding context we need to templates.
    """
    payload = {}
    payload['current_term'] = current_term()
    payload['csrf_token'] = csrf(request)['csrf_token']
    return payload


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
        """
        Overrides the get_queryset method on this model manager.
        """
        return super(ValidCasesManager, self).get_queryset()\
            .filter(decisiontype__in=["1", "7"])\
            .filter(docketid__endswith="-01")\
            .filter(caseissuesid__endswith="-01")\


class BaseScotusModel(models.Model):
    """
    A base model class for our SCOTUS models to inherit.
    Abstracts out some methods and such.
    """
    class Meta:
        abstract = True

    def dict(self):
        """
        A sane method for returning a dict from a Django model.
        """
        serialized = serializers.serialize('json', [self])
        payload = dict(json.loads(serialized)[0]['fields'])
        payload['pk'] = json.loads(serialized)[0]['pk']
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

    def smart_dict(self):
        """
        A cleaner, smartypants-ified dict.
        """
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

    def json(self):
        """
        Quickie JSON method.
        """
        return json.dumps(self.dict())

    def __str__(self):
        return self.__unicode__()


def webfix_unicode(possible_string):
    """
    This is ugly but it will create Times-approved HTML
    out of terrible cut-and-paste from decision text.
    """
    character_map = [
        ('\xa7', '&sect;'),
        ('\u2014', '&mdash;'),
        ('\u2013', '&ndash;'),
        ('\x97', '&mdash;'),
        ('\xa4', '&euro;'),
        ('\u201c', '"'),
        ('\u201d', '"'),
        ('\x96', '&#150;'),
    ]

    if isinstance(possible_string, str):
        string = possible_string
        string = string.strip()
        for char, replace_char in character_map:
            string = string.replace(char, replace_char)
        string = string.decode('utf-8')
        string = ftfy.fix_text(string)
        string = smartypants.smartypants(string)
        return string

    return possible_string
