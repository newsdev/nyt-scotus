# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0010_naturalcourt_common_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturalcourt',
            name='end_date',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='naturalcourt',
            name='start_date',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
