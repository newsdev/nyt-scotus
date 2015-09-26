# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0014_vote_decisiondirection'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='nyt_weighted_majvotes',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
