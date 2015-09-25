# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0004_auto_20150924_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='meritscase',
            name='nyt_weighted_majvotes',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
