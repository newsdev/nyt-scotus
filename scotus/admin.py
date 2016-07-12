from django.contrib import admin

from scotus import models

admin.site.register(models.OverrideCase)
admin.site.register(models.OverrideJustice)
