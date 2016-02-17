# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0025_auto_20150821_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='notice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('message', models.TextField(null=True, blank=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('attachment', models.FileField(upload_to=b'attachments')),
                ('password', models.CharField(max_length=100, null=True, blank=True)),
                ('member_recipients', models.ManyToManyField(to='pds_v3.AppUser', null=True, blank=True)),
                ('presenter_recipients', models.ManyToManyField(to='pds_v3.Presenter', null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 21, 11, 53, 42, 984738)),
        ),
    ]
