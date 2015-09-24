# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0003_remove_justiceterm_median_justice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='justiceterm',
            options={'ordering': ('-term', 'justice')},
        ),
        migrations.AddField(
            model_name='vote',
            name='term',
            field=models.CharField(db_index=True, max_length=255, null=True, blank=True),
        ),
    ]
