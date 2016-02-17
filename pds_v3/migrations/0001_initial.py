# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('terms', models.BooleanField()),
                ('img', models.ImageField(upload_to=b'', blank=True)),
                ('is_presenter', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='LawSociety',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('eligibility', models.TextField()),
                ('overview', models.TextField()),
                ('website', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='LawSocietyOverride',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('eligibility', models.TextField(default=False)),
                ('description', models.TextField(blank=True)),
                ('short_name', models.TextField(blank=True)),
                ('web_address', models.TextField(blank=True)),
                ('parent', models.ForeignKey(to='pds_v3.LawSociety', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PdSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('approved', models.BooleanField(default=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('audio_file', models.FileField(upload_to=b'audio_files')),
                ('release_date', models.DateField(auto_now_add=True)),
                ('price', models.FloatField(null=True, blank=True)),
                ('duration', models.TextField(null=True)),
                ('suspended', models.BooleanField(default=False)),
                ('archived', models.BooleanField(default=False)),
                ('lawsocietyoverrides', models.ManyToManyField(to='pds_v3.LawSocietyOverride', null=True, blank=True)),
            ],
            options={
                'verbose_name': 'PD Session',
                'verbose_name_plural': 'PD Sessions',
            },
        ),
        migrations.CreateModel(
            name='Presenter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_approved', models.DateField()),
                ('bio', models.TextField(null=True)),
                ('credentials', models.TextField(null=True, blank=True)),
                ('phone', models.CharField(max_length=100, null=True, blank=True)),
                ('law_firm', models.CharField(max_length=100, null=True, blank=True)),
                ('user', models.ForeignKey(related_name='presenter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime(2015, 7, 23, 18, 43, 30, 439379))),
                ('price', models.IntegerField()),
                ('method', models.TextField()),
                ('success', models.BooleanField(default=True)),
                ('pdsession', models.ForeignKey(to='pds_v3.PdSession')),
                ('user', models.ForeignKey(to='pds_v3.AppUser')),
            ],
        ),
        migrations.CreateModel(
            name='report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('PdSession', models.ManyToManyField(to='pds_v3.PdSession')),
                ('purchase', models.ManyToManyField(to='pds_v3.Purchase')),
                ('user', models.ManyToManyField(to='pds_v3.AppUser')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
            ],
        ),
        migrations.AddField(
            model_name='pdsession',
            name='presenters',
            field=models.ManyToManyField(to='pds_v3.Presenter', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='pdsession',
            name='subject',
            field=models.ManyToManyField(to='pds_v3.Subject', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='society',
            field=models.ManyToManyField(to='pds_v3.LawSociety', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='appuser',
            name='user',
            field=models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
