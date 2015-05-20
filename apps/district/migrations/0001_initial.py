# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=80, verbose_name=b'\xe5\x8c\xba\xe5\x9f\x9f\xe5\x90\x8d\xe7\xa7\xb0')),
                ('description', models.TextField(verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('updated', models.DateTimeField(null=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('forum_count', models.IntegerField(default=0, verbose_name=b'\xe7\x89\x88\xe5\x9d\x97\xe6\x95\xb0', blank=True)),
                ('moderators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'\xe7\x89\x88\xe4\xb8\xbb', blank=True)),
            ],
            options={
                'verbose_name': '\u533a\u57df',
                'verbose_name_plural': '\u533a\u57df',
            },
        ),
    ]
