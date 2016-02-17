# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0007_auto_20150807_2023'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('appuser', models.ManyToManyField(to='pds_v3.AppUser', blank=True)),
                ('session', models.ManyToManyField(to='pds_v3.PdSession', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 7, 20, 59, 23, 918198)),
        ),
    ]
