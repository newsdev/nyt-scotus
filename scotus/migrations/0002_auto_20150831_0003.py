# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scotus', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meritscase',
            old_name='audo_mp3',
            new_name='audio_mp3',
        ),
    ]
