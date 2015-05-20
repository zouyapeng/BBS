# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('body', models.TextField()),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': '\u641c\u7d22',
                'managed': False,
                'verbose_name_plural': '\u641c\u7d22',
            },
        ),
    ]
