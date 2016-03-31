# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0020_auto_20151005_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='courtterm',
            name='naturalcourt',
            field=models.ForeignKey(blank=True, to='scotus.NaturalCourt', null=True),
        ),
    ]
