from django.contrib import admin

from scotus import models

class JusticeAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'last_name', 'first_name']
    list_editable = ['last_name', 'first_name']

admin.site.register(models.Justice, JusticeAdmin)
admin.site.register(models.MeritsCase)
admin.site.register(models.Vote)
admin.site.register(models.CourtTerm)
admin.site.register(models.JusticeTerm)
