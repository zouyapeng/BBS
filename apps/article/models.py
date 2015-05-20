# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.loading import get_model
from django.db.models.signals import post_save
from django.utils.six import python_2_unicode_compatible

# Create your models here.
from django.utils.timezone import now
from django_extensions.db.fields import CreationDateTimeField
from jieba import posseg
import jsonfield
import markdown
from apps.attachments.models import Attachment
from apps.notifications.signals import notify
from apps.forum.models import Forum


@python_2_unicode_compatible
class Article(models.Model):
    forum = models.ForeignKey(Forum, verbose_name='板块')
    created = CreationDateTimeField("创建的时间")
    title = models.CharField("标题", max_length=255)
    body = models.TextField("文章内容")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    attachment = models.ManyToManyField(Attachment)
    update_date = models.DateTimeField('更新的时间', blank=True, null=True)
    kw = jsonfield.JSONField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        words = posseg.cut(self.title)
        words = [k.word for k in words if k.flag in ['n', 'eng'] and len(k.word) > 1]
        self.kw = words
        super(Article, self).save(force_insert, force_update, using, update_fields)

    def get_markdown(self):
        return markdown.markdown(self.body)

    def get_absolute_url(self):
        return reverse("article:detail", kwargs={"pk": self.id})

    def get_last_reply(self):
        return self.reply_set.order_by('created').last()

    class Meta(object):
        verbose_name = verbose_name_plural = '文章'

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class Reply(models.Model):
    article = models.ForeignKey(Article, verbose_name='板块')
    created = CreationDateTimeField("创建的时间")
    body = models.TextField("文章内容")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    attachment = models.ManyToManyField(Attachment)

    def get_markdown(self):
        return markdown.markdown(self.body)

    def get_absolute_url(self):
        return reverse("article:reply", kwargs={"pk": self.id})

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if created:
            instance.article.update_date = now()
            instance.article.save()
            #TODO 添加通知
            sender = get_model(settings.AUTH_USER_MODEL).objects.get(id=settings.NOTIFICATION_USER)
            notify.send(sender,
                        recipient=instance.article.user,
                        verb=u'你发起的文章[{article}]有新的回复'.format(article=instance.article.title),
                        action_object=instance,
                        description=instance.get_markdown()
            )
            from apps.account.models import Focus
            for focus in Focus.get_focus_by_content_object(instance.article).exclude(user__in=[instance.user, instance.article.user]):
                print focus.user
                notify.send(sender,
                            recipient=focus.user,
                            verb=u'你关注的文章[{article}]有新的回复'.format(article=instance.article.title),
                            action_object=instance,
                            description=instance.get_markdown()
                )

    class Meta(object):
        verbose_name = verbose_name_plural = '回复'

    def __str__(self):
        return self.body


post_save.connect(Reply.post_save, sender=Reply)