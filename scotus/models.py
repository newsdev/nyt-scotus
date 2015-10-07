from sets import Set

from django.contrib.postgres.fields import ArrayField
from django.db import models

from clerk import maps
from scotus import utils


class NaturalCourt(utils.TimeStampedMixin):
    naturalcourt = models.IntegerField(blank=True, null=True)
    common_name = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return self.naturalcourt

    def get_date_display(self):
        if self.end_date:
            return "%s - %s"  % (self.start_date, self.end_date)
        return "%s - present" % (self.start_date)


class CourtTerm(utils.TimeStampedMixin):
    """
    Represents a single term of the court for the purposes
    of aggregating the Martin-Quinn score for this court
    on this term.
    """
    term = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    martin_quinn_score = models.FloatField(null=True, blank=True)

    def __unicode__(self):
        return "%s %s" % (self.term, self.martin_quinn_score)


class MeritsCase(utils.TimeStampedMixin):
    """
    Represents a single merits case before the court.
    Largely derived from SCDB data.
    Use MeritsCase.valid_objects when doing votes because
    combined cases might appear as duplicates.
    """
    nyt_casename = models.CharField(max_length=255, null=True, blank=True)
    nyt_weighted_majvotes = models.IntegerField(blank=True, null=True)
    term = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    docket = models.CharField(max_length=255, null=True, blank=True)
    caseid = models.CharField(max_length=255, null=True, blank=True)
    docketid = models.CharField(max_length=255, null=True, blank=True)
    caseissuesid = models.CharField(max_length=255, null=True, blank=True)
    datedecision = models.DateField(blank=True, null=True)
    dategranted = models.DateField(blank=True, null=True)
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
    case_code = models.CharField(max_length=255, null=True, blank=True)
    court_originated = models.CharField(max_length=255, null=True, blank=True)
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
    question = models.TextField(blank=True, null=True)

    objects = models.Manager()
    valid_objects = utils.ValidCasesManager()

    class Meta:
        ordering = ['-term', 'casename']

    def __unicode__(self):
        if self.nyt_casename:
            return unicode(self.nyt_casename)
        return unicode(self.casename)

    def votes(self):
        if self.majvotes and self.minvotes:
            return "%s-%s" % (self.majvotes, self.minvotes)
        return None


class Justice(utils.TimeStampedMixin):
    """
    Represents a single supreme court justice.
    We have justice data from 1946 to present.
    Much of this data is incomplete and will need
    to be hand-edited, e.g., 'current' or the
    various dates for nomination / confirmation.
    """
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
        return self.get_name()

    def get_name(self):
        if self.first_name and self.last_name:
            return "%s %s" % (self.first_name, self.last_name)
        if self.full_name:
            return unicode(self.full_name)
        return unicode(self.justicename)

    def common_cases(self, justices, term=None, naturalcourt=None, maxvotes=None):
        """
        Cases this Justice and all Justices in the list `justices` have in common.
        """
        positions = Vote.active_objects.all()
        if term:
            positions = positions.filter(term=term)
        if naturalcourt:
            positions = positions.filter(naturalcourt=naturalcourt)
        if maxvotes:
            maxvotes = maxvotes.split(',')
            positions = positions.filter(majvotes__in=maxvotes)
        votes = []
        votes.append(Set([p['caseid'] for p in positions.filter(justice=self.justice).values('caseid')]))
        for j in justices:
            votes.append(Set([p['caseid'] for p in positions.filter(last_name=j).values('caseid')]))

        intersecting_cases = votes[0]
        for justice_case in votes[1:]:
            list(intersecting_cases.intersection(justice_case))
        return intersecting_cases

    def agree_positions(self, justices, cc):
        """
        Votes where this Justice and all Justices in the list `justices` were in the majority.
        """
        votes = []
        votes.append(Set([p['caseid'] for p in Vote.active_objects.filter(justice=self.justice, caseid__in=cc, vote__in=['1', '3', '4', '5']).values('caseid')]))

        for j in justices:
            votes.append(Set([p['caseid'] for p in Vote.active_objects.filter(last_name=j, caseid__in=cc, vote__in=['1', '3', '4', '5']).values('caseid')]))

        intersecting_votes = votes[0]
        for vote in votes[1:]:
            intersecting_votes = intersecting_votes.intersection(vote)

        return  (len(list(intersecting_votes)), intersecting_votes)

    def disagree_positions(self, justices, cc):
        """
        Votes where this Justice and all Justices in the list `justices` were in the minority.
        """
        votes = []
        votes.append(Set([p['caseid'] for p in Vote.active_objects.filter(justice=self.justice, caseid__in=cc, vote__in=['2']).values('caseid')]))

        for j in justices:
            votes.append(Set([p['caseid'] for p in Vote.active_objects.filter(last_name=j, caseid__in=cc, vote__in=['2']).values('caseid')]))

        intersecting_votes = votes[0]
        for vote in votes[1:]:
            intersecting_votes = intersecting_votes.intersection(vote)

        return (len(list(intersecting_votes)), intersecting_votes)


class Vote(utils.TimeStampedMixin):
    """
    Represents a single justice's position on a single merits
    case. Largely derived from SCDB data, so only for cases from
    1946-present.
    """
    term = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    naturalcourt = models.CharField(choices=maps.NATURAL_COURT_CHOICES, max_length=255, db_index=True, blank=True, null=True)
    justice = models.CharField(max_length=255, db_index=True)
    justicename = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, null=True, blank=True, db_index=True)
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
    majvotes = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    minvotes = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    decisiondirection = models.CharField(max_length=255, null=True, blank=True, db_index=True)
    nyt_weighted_majvotes = models.IntegerField(blank=True, null=True)
    caseissuesid = models.CharField(max_length=255, null=True, blank=True)
    decisiontype = models.CharField(max_length=255, null=True, blank=True)
    datedecision = models.DateField(blank=True, null=True)

    valid_objects = utils.ValidCasesManager()

    def __unicode__(self):
        return "%s in %s" % (self.justice_obj(), self.case_obj())

    def justice_obj(self):
        if Justice.objects.filter(justice=self.justice).count() == 1:
            return Justice.objects.get(justice=self.justice)
        return self.justice

    def case_obj(self):
        if MeritsCase.objects.filter(caseid=self.caseid).count() == 1:
            return MeritsCase.objects.get(caseid=self.caseid)
        return self.casename

    def is_majority(self):
        if self.majority == "1":
            return False
        if self.majority == "2":
            return True
        return None

class JusticeTerm(utils.TimeStampedMixin):
    """
    Represents a single justice's record in a single term.
    Will be nice to denormalize votes to here. Also contains
    a Martin-Quinn score for this term.
    """
    justice = models.CharField(max_length=255, db_index=True)
    term = models.CharField(max_length=255, db_index=True)
    martin_quinn_score = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ('-term', 'justice')

    def __unicode__(self):
        return "%s (%s)" % (self.justice_obj(), self.term)

    def justice_obj(self):
        if Justice.objects.filter(justice=self.justice).count() == 1:
            return Justice.objects.get(justice=self.justice)
        return self.justice

    def votes(self):
        return Vote.objects.filter(
                        justice=self.justice,
                        caseid__in=[c['caseid'] for c in Case.valid_objects.filter(term=self.term).values('caseid')])
