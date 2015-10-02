# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0015_vote_nyt_weighted_majvotes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='naturalcourt',
            name='naturalcourt',
        ),
    ]
