# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0016_auto_20150819_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdSessionEdit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('name', models.CharField(max_length=60, null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 19, 14, 54, 6, 114988)),
        ),
    ]
