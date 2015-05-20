# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.six import python_2_unicode_compatible
from apps.attachments.models import Attachment, attachment_upload
from apps.tag.models import Tag
from apps.district.models import District
from django.contrib import admin


@python_2_unicode_compatible
class Forum(models.Model):
    district = models.ForeignKey(District, verbose_name='所属区域', blank=True, null=True)
    icon = models.ImageField("图标", upload_to=attachment_upload, default="default.png")
    name = models.CharField('版块名称', max_length=80)
    description = models.TextField('描述', blank=True)
    moderators = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, verbose_name='版主')
    updated = models.DateTimeField('更新的时间', blank=True, null=True)
    post_count = models.IntegerField('回复数', blank=True, default=0)
    topic_count = models.IntegerField('主题数', blank=True, default=0)

    class Meta(object):
        verbose_name = verbose_name_plural = '版块'

    def __str__(self):
        return self.name

# admin.site.register(Forum)
