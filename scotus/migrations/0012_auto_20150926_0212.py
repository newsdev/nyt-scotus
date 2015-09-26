# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0011_auto_20150926_0209'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naturalcourt',
            name='end_date',
        ),
        migrations.RemoveField(
            model_name='naturalcourt',
            name='start_date',
        ),
        migrations.AddField(
            model_name='naturalcourt',
            name='end_year',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='naturalcourt',
            name='start_year',
            field=models.DateField(null=True, blank=True),
        ),
    ]
