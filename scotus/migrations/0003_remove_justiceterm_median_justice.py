# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0002_auto_20150831_0003'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='justiceterm',
            name='median_justice',
        ),
    ]
