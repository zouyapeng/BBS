# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.attachments.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('district', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('icon', models.ImageField(default=b'default.png', upload_to=apps.attachments.models.attachment_upload, verbose_name=b'\xe5\x9b\xbe\xe6\xa0\x87')),
                ('name', models.CharField(max_length=80, verbose_name=b'\xe7\x89\x88\xe5\x9d\x97\xe5\x90\x8d\xe7\xa7\xb0')),
                ('description', models.TextField(verbose_name=b'\xe6\x8f\x8f\xe8\xbf\xb0', blank=True)),
                ('updated', models.DateTimeField(null=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('post_count', models.IntegerField(default=0, verbose_name=b'\xe5\x9b\x9e\xe5\xa4\x8d\xe6\x95\xb0', blank=True)),
                ('topic_count', models.IntegerField(default=0, verbose_name=b'\xe4\xb8\xbb\xe9\xa2\x98\xe6\x95\xb0', blank=True)),
                ('district', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe5\x8c\xba\xe5\x9f\x9f', blank=True, to='district.District', null=True)),
                ('moderators', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'\xe7\x89\x88\xe4\xb8\xbb', blank=True)),
            ],
            options={
                'verbose_name': '\u7248\u5757',
                'verbose_name_plural': '\u7248\u5757',
            },
        ),
    ]
