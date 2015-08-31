from django.contrib.postgres.fields import ArrayField
from django.db import models

from scotus import maps
from scotus import utils


class CourtTerm(utils.TimeStampedMixin):
    term = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    martin_quinn_score = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.term, self.martin_quinn_score)


class MeritsCase(utils.TimeStampedMixin):
    nyt_courtterm = models.ForeignKey(CourtTerm, null=True, blank=True)
    nyt_casename = models.CharField(max_length=255, null=True, blank=True)
    term = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    docket = models.CharField(max_length=255, null=True, blank=True)
    caseid = models.CharField(max_length=255, null=True, blank=True)
    docketid = models.CharField(max_length=255, null=True, blank=True)
    caseissuesid = models.CharField(max_length=255, null=True, blank=True)
    datedecision = models.DateField(blank=True, null=True)
    decisiontype = models.CharField(choices=maps.DECISION_TYPE_CHOICES, max_length=255, null=True, blank=True)
    uscite = models.CharField(max_length=255, null=True, blank=True)
    sctcite = models.CharField(max_length=255, null=True, blank=True)
    ledcite = models.CharField(max_length=255, null=True, blank=True)
    lexiscite = models.CharField(max_length=255, null=True, blank=True)
    naturalcourt = models.CharField(choices=maps.NATURAL_COURT_CHOICES, max_length=255, db_index=True)
    chief = models.CharField(max_length=255, null=True, blank=True)
    casename = models.CharField(max_length=255, null=True, blank=True)
    dateargument = models.DateField(blank=True, null=True)
    daterearg = models.DateField(blank=True, null=True)
    petitioner = models.CharField(choices=maps.PETITIONER_RESPONDENT_CHOICES, max_length=255, db_index=True, blank=True, null=True)
    petitionerstate = models.CharField(choices=maps.STATE_CHOICES, max_length=255, blank=True, null=True)
    respondent = models.CharField(choices=maps.PETITIONER_RESPONDENT_CHOICES, max_length=255, blank=True, null=True)
    respondentstate = models.CharField(choices=maps.STATE_CHOICES, max_length=255, blank=True, null=True)
    jurisdiction = models.CharField(choices=maps.JURISDICTION_CHOICES, max_length=255, db_index=True, null=True, blank=True)
    adminaction = models.CharField(choices=maps.ADMINISTRATIVE_ACTION_CHOICES, max_length=255, null=True, blank=True)
    adminactionstate = models.CharField(choices=maps.STATE_CHOICES, max_length=255, null=True, blank=True)
    threejudgefdc = models.CharField(choices=maps.THREE_JUDGE_DISTRICT_COURT_CHOICES, max_length=255, null=True, blank=True)
    caseorigin = models.CharField(choices=maps.CASE_ORIGIN_CHOICES, max_length=255, null=True, blank=True)
    caseoriginstate = models.CharField(choices=maps.STATE_CHOICES, max_length=255, null=True, blank=True)
    casesource = models.CharField(choices=maps.CASE_ORIGIN_CHOICES, max_length=255, null=True, blank=True)
    casesourcestate = models.CharField(choices=maps.STATE_CHOICES, max_length=255, null=True, blank=True)
    certreason = models.CharField(choices=maps.CERT_REASON_OPTIONS, max_length=255, null=True, blank=True)
    lcdisagreement = models.CharField(choices=maps.LOWER_COURT_AGREEMENT_CHOICES, max_length=255, null=True, blank=True)
    lcdisposition = models.CharField(choices=maps.LOWER_COURT_DISPOSITION_CHOICES, max_length=255, null=True, blank=True)
    lcdispositiondirection = models.CharField(choices=maps.DECISION_DIRECTION_CHOICES, max_length=255, null=True, blank=True)
    lcdecisiondirection = models.CharField(choices=maps.DECISION_DIRECTION_CHOICES, max_length=255, null=True, blank=True)
    declarationuncon = models.CharField(choices=maps.UNCONSTITUTIONALITY_CHOICES, max_length=255, null=True, blank=True)
    casedisposition = models.CharField(choices=maps.CASE_DISPOSITION_CHOICES, max_length=255, null=True, blank=True)
    casedispositionunusual = models.CharField(choices=maps.CASE_DISPOSITION_UNUSUAL_CHOICES, max_length=255, null=True, blank=True)
    partywinning = models.CharField(choices=maps.WINNING_PARTY_CHOICES, max_length=255, null=True, blank=True)
    precedentalteration = models.CharField(choices=maps.PRECEDENT_ALTERATION_CHOICES, max_length=255, null=True, blank=True)
    voteunclear = models.CharField(choices=maps.VOTE_UNCLEAR_CHOICES, max_length=255, null=True, blank=True)
    issue = models.CharField(choices=maps.ISSUE_CHOICES, max_length=255, blank=True, null=True, db_index=True)
    issuearea = models.CharField(choices=maps.ISSUE_AREA_CHOICES, max_length=255, blank=True, null=True, db_index=True)
    decisiondirection = models.CharField(choices=maps.DECISION_DIRECTION_CHOICES, max_length=255, db_index=True, null=True, blank=True)
    decisiondirectiondissent = models.CharField(choices=maps.DECISION_DIRECTION_DISSENT_CHOICES, max_length=255, db_index=True, null=True, blank=True)
    authoritydecision1 = models.CharField(choices=maps.DECISION_AUTHORITY_CHOICES, max_length=255, null=True, blank=True)
    authoritydecision2 = models.CharField(choices=maps.DECISION_AUTHORITY_CHOICES, max_length=255, null=True, blank=True)
    lawtype = models.CharField(choices=maps.DECISION_LAW_TYPE_CHOICES, max_length=255, null=True, blank=True)
    lawsupp = models.CharField(choices=maps.LAW_SUPP_CHOICES, max_length=255, null=True, blank=True)
    lawminor = models.CharField(max_length=255, null=True, blank=True)
    majopinwriter = models.CharField(max_length=255, null=True, blank=True)
    majopinassigner = models.CharField(max_length=255, null=True, blank=True)
    splitvote = models.CharField(choices=maps.SPLIT_VOTE_CHOICES, max_length=255, null=True, blank=True)
    majvotes = models.CharField(max_length=255, db_index=True)
    minvotes = models.CharField(max_length=255, db_index=True)
    short_name = models.CharField(max_length=255, blank=True, null=True)
    opinion_pdf_url = models.CharField(max_length=255, blank=True, null=True)
    argument_pdf = ArrayField(models.CharField(max_length=255, blank=True, null=True), default=[])
    audio_mp3 = ArrayField(models.CharField(max_length=255, blank=True, null=True), default=[])
    valid_cases = utils.ValidCasesManager()

    def __unicode__(self):
        if self.nyt_casename:
            return unicode(self.nyt_casename)
        return unicode(self.casename)


class Justice(utils.TimeStampedMixin):
    justice = models.CharField(max_length=255)
    justicename = models.CharField(max_length=255)
    current = models.BooleanField(default=False)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    nominated = models.DateField(null=True, blank=True)
    confirmed = models.DateField(null=True, blank=True)
    sworn_in = models.DateField(null=True, blank=True)
    was_chief = models.BooleanField(default=False)
    active_terms = models.TextField(blank=True, null=True)
    first_term = models.CharField(max_length=255, null=True, blank=True)
    last_term = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    segal_cover_ideology_score = models.FloatField(null=True, blank=True)
    segal_cover_qualification_score = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        if self.full_name:
            return unicode(self.full_name)
        return unicode(self.justicename)


class Vote(utils.TimeStampedMixin):
    justice = models.CharField(max_length=255, db_index=True)
    justicename = models.CharField(max_length=255, db_index=True)
    caseid = models.CharField(max_length=255, db_index=True)
    docketid = models.CharField(max_length=255, db_index=True)
    casename = models.CharField(max_length=255, null=True, blank=True)
    vote = models.CharField(choices=maps.VOTE_CHOICES, max_length=255, null=True, blank=True, db_index=True)
    opinion = models.CharField(choices=maps.WROTE_OPINION_CHOICES, max_length=255, null=True, blank=True, db_index=True)
    direction = models.CharField(choices=maps.DECISION_DIRECTION_CHOICES, max_length=255, null=True, blank=True, db_index=True)
    majority = models.CharField(choices=(("1", "Dissent"), ("2", "Majority")), max_length=255, null=True, blank=True, db_index=True)
    firstagreement = models.CharField(max_length=255, null=True, blank=True)
    secondagreement = models.CharField(max_length=255, null=True, blank=True)
    voteid = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.justicename, self.casename)


class JusticeTerm(utils.TimeStampedMixin):
    justice = models.CharField(max_length=255, db_index=True)
    term = models.CharField(max_length=255, db_index=True)
    martin_quinn_score = models.FloatField(null=True, blank=True)
    median_justice = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s %s %s" % (self.justice, self.term, self.martin_quinn_score)

    def votes(self):
        return Vote.objects.filter(
                        justice=self.justice,
                        caseid__in=[c['caseid'] for c in Case.valid_cases.filter(term=self.term).values('caseid')])