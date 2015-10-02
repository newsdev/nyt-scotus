# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0017_naturalcourt_naturalcourt'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='caseissuesid',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='datedecision',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='decisiontype',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
