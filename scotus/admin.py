from django.contrib import admin

from scotus import models

admin.site.register(models.Justice)
admin.site.register(models.MeritsCase)
admin.site.register(models.Vote)
admin.site.register(models.CourtTerm)
admin.site.register(models.JusticeTerm)
