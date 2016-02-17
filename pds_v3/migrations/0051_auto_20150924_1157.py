# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('pds_v3', '0050_auto_20150910_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdAudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=b'100', null=True, blank=True)),
                ('audio', models.FileField(null=True, upload_to=b'pd_audio', blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='presenter',
            name='image',
            field=models.FileField(null=True, upload_to=b'pds_v3/static/presenter_pics', blank=True),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 24, 11, 57, 9, 709572)),
        ),
    ]
