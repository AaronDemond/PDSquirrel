# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0010_auto_20150807_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Completed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('proof', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 21, 24, 41, 198358)),
        ),
    ]
