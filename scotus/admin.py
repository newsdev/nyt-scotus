from django.contrib import admin

from scotus import models

class CourtTermAdmin(admin.ModelAdmin):
    list_display = ['term', 'med']

class MeritsCaseAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'docket', 'term', 'datedecision']
    search_fields = ['casename', 'weighted_majvotes', 'docket']

class JusticeAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'justice']

admin.site.register(models.Justice, JusticeAdmin)
admin.site.register(models.NaturalCourt)
admin.site.register(models.MeritsCase, MeritsCaseAdmin)
admin.site.register(models.Vote)
admin.site.register(models.CourtTerm, CourtTermAdmin)
admin.site.register(models.JusticeTerm)
