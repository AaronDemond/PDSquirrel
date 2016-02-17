# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0041_auto_20150901_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presenter',
            name='user',
            field=models.OneToOneField(related_name='presenter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 1, 14, 55, 10, 410791)),
        ),
    ]
