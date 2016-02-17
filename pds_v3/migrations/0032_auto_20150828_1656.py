# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0031_auto_20150828_1654'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pdattachment',
            old_name='file',
            new_name='attachment',
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 28, 16, 56, 25, 20122)),
        ),
    ]
