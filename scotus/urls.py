from django.conf.urls import patterns, include, url
from django.contrib import admin

from scotus import views


urlpatterns = patterns('',
    (r'^scotus/admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^api/v1/case/nyt/filter/$', views.filter_and_sum_api),
    url(r'^api/v1/voting/justice/(?P<last_name>\w+)/', views.voting_clusters, name='voting-clusters'),
    url(r'^api/v1/case/by-court/$', views.cases_by_court),
    url(r'^api/v1/case/by-term/$', views.cases_by_term),
)