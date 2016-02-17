# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0035_auto_20150831_1059'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipCancellationRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(null=True, blank=True)),
                ('user', models.ForeignKey(to='pds_v3.AppUser', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MembershipPaymentRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ammount', models.FloatField(null=True, blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('method', models.CharField(max_length=200, null=True, blank=True)),
                ('success', models.BooleanField()),
                ('monthly_credits', models.IntegerField(null=True, blank=True)),
                ('user', models.ForeignKey(to='pds_v3.AppUser', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 11, 10, 7, 694275)),
        ),
    ]
