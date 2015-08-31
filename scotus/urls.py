from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    (r'^scotus/admin/', include(admin.site.urls)),
)