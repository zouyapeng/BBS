# -*- coding: utf-8 -*-
import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django_extensions.db.fields import CreationDateTimeField


@python_2_unicode_compatible
class Tag(models.Model):
    created = CreationDateTimeField("创建的时间")
    title = models.CharField("名称", max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    avatar = models.ImageField("图标", default="tag-default.png")
    describe = models.TextField("描述", null=True, blank=True)
    update_date = models.DateTimeField(default=now())

    def get_absolute_url(self):
        return reverse("tag:tag_detail", kwargs={"title": self.title})

    def get_week_count(self):
        return self.question_set.filter(created__gt=now()-datetime.timedelta(days=7)).count()+self.article_set.filter(created__gt=now()-datetime.timedelta(days=7)).count()

    def get_30_count(self):
        return self.question_set.filter(created__gt=now()-datetime.timedelta(days=30)).count()+self.article_set.filter(created__gt=now()-datetime.timedelta(days=30)).count()

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = verbose_name_plural = '标签'


