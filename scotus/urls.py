from django.conf.urls import include, url
from django.contrib import admin

from scotus import views

UTIL = (
    url(r'^admin/', include(admin.site.urls)),
)

HTML = (
    url(r'^justice/(?P<justiceid>\d+)/$', views.justice_detail),
    url(r'^case/(?P<caseissuesid>\w+)/$', views.case_detail),
    url(r'^case/$', views.case_list),
    url(r'^$', views.index),
)

API = (
    url(r'^api/v1/justice/liberal/(?P<term>\d+)/$', views.liberal_decisions_by_justice),
    url(r'^api/v1/score/justice/$', views.justice_scores_by_term),
    url(r'^api/v1/case/filter/$', views.filter_and_sum_api),
    url(r'^api/v1/voting/justice/(?P<justicename>\w+)/', views.voting_clusters, name='voting-clusters'),
    url(r'^api/v1/case/by-term/$', views.cases_by_term),
    url(r'^api/v1/case/by-court/$', views.cases_by_court),
    url(r'^api/v1/score/naturalcourt/$', views.scores_by_natural_court),
    url(r'^api/v1/score/court/$', views.court_scores_by_term),
)

urlpatterns = UTIL + API + HTML
