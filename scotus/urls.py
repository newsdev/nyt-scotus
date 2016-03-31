from django.conf.urls import patterns, include, url
from django.contrib import admin

from scotus import views


urlpatterns = patterns('',
    (r'^scotus/admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^scotus/api/v1/justice/liberal_pct/(?P<term>\d+)/', views.liberal_decisions_by_justice),
    url(r'^scotus/api/v1/score/naturalcourt/$', views.scores_by_natural_court),
    url(r'^scotus/api/v1/score/court/$', views.court_scores_by_term),
    url(r'^scotus/api/v1/score/justice/$', views.justice_scores_by_term),
    url(r'^scotus/api/v1/case/nyt/filter/$', views.filter_and_sum_api),
    url(r'^scotus/api/v1/voting/justice/(?P<last_name>\w+)/', views.voting_clusters, name='voting-clusters'),
    url(r'^scotus/api/v1/case/by-court/$', views.cases_by_court),
    url(r'^scotus/api/v1/case/by-term/$', views.cases_by_term),
)