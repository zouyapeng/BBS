# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.attachments.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('source_filename', models.CharField(verbose_name=b'Source Filename', max_length=255, null=True, editable=False, blank=True)),
                ('target_filename', models.CharField(verbose_name=b'Target Filename', max_length=255, null=True, editable=False, blank=True)),
                ('attachment_file', models.FileField(upload_to=apps.attachments.models.attachment_upload, verbose_name='attachment')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('creator', models.ForeignKey(related_name='created_attachments', verbose_name=b'\xe6\x96\x87\xe4\xbb\xb6\xe4\xb8\x8a\xe4\xbc\xa0\xe8\x80\x85', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'permissions': (('delete_foreign_attachments', 'Can delete foreign attachments'),),
            },
        ),
    ]
