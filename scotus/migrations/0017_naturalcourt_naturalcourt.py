# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0016_remove_naturalcourt_naturalcourt'),
    ]

    operations = [
        migrations.AddField(
            model_name='naturalcourt',
            name='naturalcourt',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
