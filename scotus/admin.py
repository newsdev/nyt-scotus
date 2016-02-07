from django.contrib import admin

from scotus import models

class MeritsCaseAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'docket', 'term', 'nyt_weighted_majvotes', 'datedecision']
    search_fields = ['casename', 'nyt_casename', 'docket']

class JusticeAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'last_name', 'first_name', 'justice']

admin.site.register(models.Justice, JusticeAdmin)
admin.site.register(models.NaturalCourt)
admin.site.register(models.MeritsCase, MeritsCaseAdmin)
admin.site.register(models.Vote)
admin.site.register(models.CourtTerm)
admin.site.register(models.JusticeTerm)
