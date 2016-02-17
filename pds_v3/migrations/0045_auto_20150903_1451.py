# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0044_auto_20150902_1456'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street_address', models.CharField(max_length=255, null=True, blank=True)),
                ('street_address_2', models.CharField(max_length=255, null=True, blank=True)),
                ('po_box', models.CharField(max_length=10, null=True, blank=True)),
                ('municipality', models.CharField(max_length=255, null=True, blank=True)),
                ('province', models.CharField(max_length=10, null=True, blank=True)),
                ('postal_code', models.CharField(max_length=100, null=True, blank=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='pdsessionedit',
            options={'get_latest_by': 'date'},
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 3, 14, 51, 31, 658294)),
        ),
        migrations.AddField(
            model_name='appuser',
            name='address',
            field=models.ForeignKey(blank=True, to='pds_v3.Address', null=True),
        ),
    ]
