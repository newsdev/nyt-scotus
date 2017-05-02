from django.conf.urls import include, url
from django.contrib import admin

from scotus import views

UTIL = (
    url(r'^scotus/admin/', include(admin.site.urls)),
)

HTML = (
    url(r'^scotus/justice/edit/(?P<justiceid>\d+)/$', views.edit_justice),
    url(r'^scotus/case/edit/(?P<caseissuesid>\w+)/$', views.edit_case),
    url(r'^scotus/case/current/$', views.resolve_current_cases),
    url(r'^scotus/$', views.index),
)

API = (
    url(r'^scotus/api/v1/justice/liberal/(?P<term>\d+)/$', views.liberal_decisions_by_justice),
    url(r'^scotus/api/v1/score/justice/$', views.justice_scores_by_term),
    url(r'^scotus/api/v1/case/filter/$', views.filter_and_sum_api),
    url(r'^scotus/api/v1/voting/justice/(?P<justicename>\w+)/', views.voting_clusters, name='voting-clusters'),
    url(r'^scotus/api/v1/case/by-term/$', views.cases_by_term),
    url(r'^scotus/api/v1/case/by-court/$', views.cases_by_court),
    url(r'^scotus/api/v1/score/naturalcourt/$', views.scores_by_natural_court),
    url(r'^scotus/api/v1/score/court/$', views.court_scores_by_term),
)

urlpatterns = UTIL + API + HTML
