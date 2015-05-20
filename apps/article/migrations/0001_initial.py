# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_extensions.db.fields
import jsonfield.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('attachments', '0001_initial'),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('title', models.CharField(max_length=255, verbose_name=b'\xe6\xa0\x87\xe9\xa2\x98')),
                ('body', models.TextField(verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x86\x85\xe5\xae\xb9')),
                ('update_date', models.DateTimeField(null=True, verbose_name=b'\xe6\x9b\xb4\xe6\x96\xb0\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', blank=True)),
                ('kw', jsonfield.fields.JSONField(default=dict)),
                ('attachment', models.ManyToManyField(to='attachments.Attachment')),
                ('forum', models.ForeignKey(verbose_name=b'\xe6\x9d\xbf\xe5\x9d\x97', to='forum.Forum')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('body', models.TextField(verbose_name=b'\xe6\x96\x87\xe7\xab\xa0\xe5\x86\x85\xe5\xae\xb9')),
                ('article', models.ForeignKey(verbose_name=b'\xe6\x9d\xbf\xe5\x9d\x97', to='article.Article')),
                ('attachment', models.ManyToManyField(to='attachments.Attachment')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u56de\u590d',
                'verbose_name_plural': '\u56de\u590d',
            },
        ),
    ]
