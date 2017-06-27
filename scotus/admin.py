from django.contrib import admin

from scotus import models

@admin.register(models.Case)
class CaseAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Justice)
class JusticeAdmin(admin.ModelAdmin):
    pass

@admin.register(models.Vote)
class VoteAdmin(admin.ModelAdmin):
    pass
