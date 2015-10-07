# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0019_auto_20151005_1132'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='meritscase',
            options={'ordering': ['-term', 'casename']},
        ),
        migrations.AddField(
            model_name='meritscase',
            name='question',
            field=models.TextField(null=True, blank=True),
        ),
    ]
