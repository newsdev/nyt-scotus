# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0012_auto_20150926_0212'),
    ]

    operations = [
        migrations.RenameField(
            model_name='naturalcourt',
            old_name='end_year',
            new_name='end_date',
        ),
        migrations.RenameField(
            model_name='naturalcourt',
            old_name='start_year',
            new_name='start_date',
        ),
    ]
