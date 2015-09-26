# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0009_naturalcourt'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturalcourt',
            name='common_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
