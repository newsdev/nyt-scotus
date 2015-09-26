# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0007_vote_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='majvotes',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='vote',
            name='minvotes',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]
