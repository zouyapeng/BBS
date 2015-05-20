# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.account.models
import django_extensions.db.fields
import django.contrib.auth.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('openid', models.IntegerField(null=True, blank=True)),
                ('avatar', models.ImageField(default=b'default.png', upload_to=apps.account.models.attachment_upload, verbose_name=b'\xe5\xa4\xb4\xe5\x83\x8f')),
                ('sex', models.CharField(default=b'secrecy', max_length=10, choices=[(b'man', b'man'), (b'female', b'female'), (b'secrecy', b'secrecy')])),
                ('birthday', models.DateField(null=True, blank=True)),
                ('signature', models.TextField(null=True, blank=True)),
                ('qq', models.CharField(max_length=255, null=True, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': '\u7528\u6237',
                'swappable': 'AUTH_USER_MODEL',
                'verbose_name_plural': '\u7528\u6237',
            },
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Accuracy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u4e0d\u662f\u7b54\u6848',
                'verbose_name_plural': '\u4e0d\u662f\u7b54\u6848',
            },
        ),
        migrations.CreateModel(
            name='AnswerVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('agree', models.BooleanField(default=False)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6295\u7968',
                'verbose_name_plural': '\u7528\u6237\u6295\u7968',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('body', models.TextField(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe7\x9a\x84\xe5\x86\x85\xe5\xae\xb9')),
                ('object_id', models.PositiveIntegerField(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\xaf\xb9\xe8\xb1\xa1\xe7\x9a\x84ID')),
                ('content_type', models.ForeignKey(verbose_name=b'\xe8\xaf\x84\xe8\xae\xba\xe5\xaf\xb9\xe8\xb1\xa1\xe7\x9a\x84\xe7\xb1\xbb\xe5\x9e\x8b', to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u8bc4\u8bba',
                'verbose_name_plural': '\u8bc4\u8bba',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u6536\u85cf',
                'verbose_name_plural': '\u7528\u6237\u6536\u85cf',
            },
        ),
        migrations.CreateModel(
            name='Focus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u5173\u6ce8',
                'verbose_name_plural': '\u7528\u6237\u5173\u6ce8',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('ip', models.GenericIPAddressField(default=b'0.0.0.0')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u8bb0\u5f55',
                'verbose_name_plural': '\u8bb0\u5f55',
            },
        ),
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField(verbose_name=b'\xe9\x82\x80\xe8\xaf\xb7\xe5\xaf\xb9\xe8\xb1\xa1\xe7\x9a\x84ID')),
                ('content_type', models.ForeignKey(verbose_name=b'\xe9\x82\x80\xe8\xaf\xb7\xe5\xaf\xb9\xe8\xb1\xa1\xe7\x9a\x84\xe7\xb1\xbb\xe5\x9e\x8b', to='contenttypes.ContentType')),
                ('recipient', models.ForeignKey(verbose_name=b'\xe8\xa2\xab\xe9\x82\x80\xe8\xaf\xb7\xe4\xba\xba', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='invites', verbose_name=b'\xe9\x82\x80\xe8\xaf\xb7\xe4\xba\xba', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u9080\u8bf7',
                'verbose_name_plural': '\u7528\u6237\u9080\u8bf7',
            },
        ),
        migrations.CreateModel(
            name='Thank',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe6\x97\xb6\xe9\x97\xb4', editable=False, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name=b'\xe5\x88\x9b\xe5\xbb\xba\xe7\x9a\x84\xe7\x94\xa8\xe6\x88\xb7', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u7528\u6237\u611f\u8c22',
                'verbose_name_plural': '\u7528\u6237\u611f\u8c22',
            },
        ),
    ]
