# -*- coding: utf-8 -*-
import os
import uuid
from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.utils.six import python_2_unicode_compatible
from django.utils.timezone import now
from django_extensions.db.fields import CreationDateTimeField


def attachment_upload(instance, filename):
    file_name = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    return os.path.join(settings.ATTACHMENT_UPLOAD_TO, file_name)


class User(AbstractUser):
    openid = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField("头像", upload_to=attachment_upload, default="default.png")
    sex = models.CharField(choices=(('man', 'man'), ('female', 'female'), ('secrecy', 'secrecy')), max_length=10,
                           default='secrecy')
    birthday = models.DateField(null=True, blank=True)
    signature = models.TextField(null=True, blank=True)
    qq = models.CharField(null=True, blank=True, max_length=255)


    def get_absolute_url(self):
        return reverse("account:detail", kwargs={"name": self.username})

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if created:
            # TODO 添加用户权限
            instance.user_permissions.add(*map(lambda p: Permission.objects.get_by_natural_key(*p),
                                               [['add_comment', 'account', 'comment'],
                                               ['change_accuracy', 'account', 'accuracy'],
                                                ['delete_accuracy', 'account', 'accuracy'],
                                                ['add_accuracy', 'account', 'accuracy'],
                                                ['delete_reply', 'article', 'reply'],
                                                ['change_reply', 'article', 'reply'],
                                                ['add_reply', 'article', 'reply'],
                                                ['add_article', 'article', 'article'],
                                                ['change_article', 'article', 'article'],
                                                ['delete_answervote', 'account', 'answervote'],
                                                ['change_answervote', 'account', 'answervote'],
                                                ['add_answervote', 'account', 'answervote'],
                                                ['delete_thank', 'account', 'thank'],
                                                ['change_thank', 'account', 'thank'],
                                                ['add_thank', 'account', 'thank'],
                                                ['delete_focus', 'account', 'focus'],
                                                ['change_focus', 'account', 'focus'],
                                                ['add_focus', 'account', 'focus'],
                                                ['delete_favorite', 'account', 'favorite'],
                                                ['change_favorite', 'account', 'favorite'],
                                                ['add_favorite', 'account', 'favorite'],
                                                ['add_attachment', 'attachments', 'attachment'],
                                                # ['add_questionattachment', 'question', 'questionattachment'],
                                                # ['change_questionattachment', 'question', 'questionattachment'],
                                                # ['delete_questionattachment', 'question', 'questionattachment'],
                                                # ['add_tag', 'tag', 'tag'],
                                                # ['change_tag', 'tag', 'tag'],
                                                # ['add_answer', 'question', 'answer'],
                                                # ['change_answer', 'question', 'answer'],
                                                # ['delete_answer', 'question', 'answer'],
                                                # ['add_question', 'question', 'question'],
                                                # ['change_question', 'question', 'question'],
                                                ['change_user', 'account', 'user'],
                                               ]))

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'
        verbose_name = verbose_name_plural = '用户'


post_save.connect(User.post_save, sender=User)


@python_2_unicode_compatible
class Focus(models.Model):
    created = CreationDateTimeField("创建的时间")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    @classmethod
    def get_focus_by_content_object(cls, content_object):
        return cls.objects.filter(object_id=content_object.id, content_type=ContentType.objects.get_for_model(content_object))

    def __str__(self):
        return str(self.created)

    class Meta(object):
        verbose_name = verbose_name_plural = '用户关注'


@python_2_unicode_compatible
class Favorite(models.Model):
    created = CreationDateTimeField("创建的时间")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.created)

    class Meta(object):
        verbose_name = verbose_name_plural = '用户收藏'


@python_2_unicode_compatible
class Thank(models.Model):
    created = CreationDateTimeField("创建的时间")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.created)

    class Meta(object):
        verbose_name = verbose_name_plural = '用户感谢'


@python_2_unicode_compatible
class Accuracy(models.Model):
    created = CreationDateTimeField("创建的时间")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.created)

    class Meta(object):
        verbose_name = verbose_name_plural = '不是答案'


@python_2_unicode_compatible
class AnswerVote(models.Model):
    created = CreationDateTimeField("创建的时间")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    agree = models.BooleanField(default=False)

    def __str__(self):
        return str(self.created)

    class Meta(object):
        verbose_name = verbose_name_plural = '用户投票'


@python_2_unicode_compatible
class History(models.Model):
    created = CreationDateTimeField("创建的时间")
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户', blank=True, null=True)
    ip = models.GenericIPAddressField(default='0.0.0.0')

    @classmethod
    def generate_history(cls, obj, request, interval=1*86400):
        user = None
        ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
        if request.user.is_authenticated():
            user = request.user
            history = cls.objects.filter(
                user=user,
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                created__gt=now()-timedelta(seconds=interval)
            ).order_by("created").exists()
        else:
            history = cls.objects.filter(
                content_type=ContentType.objects.get_for_model(obj),
                object_id=obj.id,
                ip=ip,
                created__gt=now()-timedelta(seconds=interval)
            ).order_by("created").exists()

        if not history:
            cls.objects.create(content_object=obj, user=user, ip=ip)

    def __str__(self):
        return str(self.created)

    class Meta(object):
        verbose_name = verbose_name_plural = '记录'


@python_2_unicode_compatible
class Invite(models.Model):
    created = CreationDateTimeField("创建的时间")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='被邀请人')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='邀请人', related_name='invites', null=True, blank=True)

    content_type = models.ForeignKey(ContentType, verbose_name="邀请对象的类型")
    object_id = models.PositiveIntegerField(verbose_name="邀请对象的ID")
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.created)

    class Meta(object):
        verbose_name = verbose_name_plural = '用户邀请'


@python_2_unicode_compatible
class Comment(models.Model):
    created = CreationDateTimeField("创建的时间")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    body = models.TextField("评论的内容")
    content_type = models.ForeignKey(ContentType, verbose_name="评论对象的类型")
    object_id = models.PositiveIntegerField(verbose_name="评论对象的ID")
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return str(self.body)

    class Meta(object):
        verbose_name = verbose_name_plural = '评论'
