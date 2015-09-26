# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0006_auto_20150925_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='last_name',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]
