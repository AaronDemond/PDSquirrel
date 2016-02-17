# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0030_auto_20150828_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='pdsession',
            name='attachments',
            field=models.ManyToManyField(to='pds_v3.PdAttachment', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 28, 16, 54, 7, 159924)),
        ),
    ]
