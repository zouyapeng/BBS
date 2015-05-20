# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.six import python_2_unicode_compatible
from apps.attachments.models import Attachment
from apps.tag.models import Tag
import uuid
import os
from django.contrib import admin


def attachment_upload(instance, filename):
    file_name = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    return os.path.join(settings.DISTRICT_ICON_UPLOAD_TO, file_name)

@python_2_unicode_compatible
class District(models.Model):
    name = models.CharField('区域名称', max_length=80)
    description = models.TextField('描述', blank=True)
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name='版主')
    updated = models.DateTimeField('更新的时间', blank=True, null=True)
    forum_count = models.IntegerField('版块数', blank=True, default=0)

    class Meta(object):
        verbose_name = verbose_name_plural = '区域'

    def __str__(self):
        return self.name

admin.site.register(District)