# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0018_auto_20151002_1426'),
    ]

    operations = [
        migrations.AddField(
            model_name='meritscase',
            name='case_code',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meritscase',
            name='court_originated',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='meritscase',
            name='dategranted',
            field=models.DateField(null=True, blank=True),
        ),
    ]
