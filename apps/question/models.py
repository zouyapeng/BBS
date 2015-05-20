# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.loading import get_model
from django.db.models.signals import post_save, pre_save
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django_extensions.db.fields import CreationDateTimeField
from jieba import posseg
import jsonfield
import markdown
from simplediff import *
from simplediff import check_diff
from apps.attachments.models import Attachment
from apps.notifications.signals import notify
from apps.tag.models import Tag
from util import summary


@python_2_unicode_compatible
class Question(models.Model):
    created = CreationDateTimeField("创建的时间")
    title = models.CharField("标题", max_length=255)
    body = models.TextField("问题补充", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    tag = models.ManyToManyField(Tag, through='QuestionTag')
    attachment = models.ManyToManyField(Attachment, through='QuestionAttachment')
    kw = jsonfield.JSONField()
    last_answer_date = models.DateTimeField('最后回复的时间', blank=True, null=True)
    answer_count = models.IntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        words = posseg.cut(self.title)
        words = [k.word for k in words if k.flag in ['n', 'eng'] and len(k.word) > 1]
        self.kw = words
        super(Question, self).save(force_insert, force_update, using, update_fields)

    def get_markdown(self):
        return markdown.markdown(self.body)

    def get_absolute_url(self):
        return reverse("question:detail", kwargs={"pk": self.id})

    def get_last_answer(self):
        return self.answer_set.order_by('created').last()

    def get_focus_user(self):
        from apps.account.models import Focus

        return Focus.objects.filter(object_id=self.id, content_type=ContentType.objects.get_for_model(self))

    def get_last_history(self):
        if not hasattr(self, '_last_history'):
            self._last_history = self.questionhistory_set.order_by('created').last()
        return self._last_history

    def get_contribute(self):
        return get_model(settings.AUTH_USER_MODEL).objects.filter(
            id__in=list(set(self.answer_set.all().order_by('-created').values_list('user_id', flat=True)))[0:3])


    def update_status(self):
        self.last_answer_date = now()
        self.answer_count = self.answer_set.count()
        self.save()

    def __str__(self):
        return self.title

    class Meta(object):
        verbose_name = verbose_name_plural = '问题'


class QuestionTag(models.Model):
    tag = models.ForeignKey(Tag)
    question = models.ForeignKey(Question, verbose_name='问题')

    def get_absolute_url(self):
        return self.tag.get_absolute_url()

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if created:
            # TODO 添加通知
            from apps.account.models import Focus
            instance.tag.update_date = now()
            instance.tag.save()

            for focus in Focus.get_focus_by_content_object(instance.tag).exclude(user=instance.question.user):
                notify.send(get_model(settings.AUTH_USER_MODEL).objects.get(id=settings.NOTIFICATION_USER),
                            recipient=focus.user,
                            verb=u'你关注的标签[{tag}]有新的问题'.format(tag=instance.tag.title),
                            action_object=instance,
                            description=instance.question.get_markdown()
                )


post_save.connect(QuestionTag.post_save, sender=QuestionTag)


class QuestionAttachment(models.Model):
    question = models.ForeignKey(Question, verbose_name='问题')
    attachment = models.ForeignKey(Attachment, verbose_name='问题')


def create_pre_question_history(sender, instance, **kwargs):
    if instance.id:
        old_question = Question.objects.get(id=instance.id)
        if old_question.title != instance.title:
            QuestionHistory(user=instance.user, question=instance, title='修改了标题', old_value=old_question.title,
                            new_value=instance.title).save()
        if old_question.body != instance.body:
            QuestionHistory(user=instance.user, question=instance, title='修改了问题内容', old_value=old_question.body,
                            new_value=instance.body).save()


def create_question_history(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, Question):
            QuestionHistory(user=instance.user, question=instance, title='添加了该问题', qescription=instance.title).save()
        elif isinstance(instance, QuestionTag):
            QuestionHistory(user=instance.question.user, question=instance.question, title='给该问题添加了一个话题',
                            qescription="<a href='%s'>%s</a>" % (
                                instance.tag.get_absolute_url(), instance.tag.title)).save()


post_save.connect(create_question_history, sender=Question)
post_save.connect(create_question_history, sender=QuestionTag)

pre_save.connect(create_pre_question_history, sender=Question)


@python_2_unicode_compatible
class QuestionHistory(models.Model):
    question = models.ForeignKey(Question, verbose_name='问题')
    created = CreationDateTimeField("创建的时间")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    title = models.CharField(max_length=255)
    qescription = models.TextField(null=True, blank=True)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)

    def get_markdown(self):
        return markdown.markdown(self.question.body)

    def get_absolute_url(self):
        return reverse("question:detail", kwargs={"pk": self.id})


    def get_qescription(self):
        if self.qescription:
            return self.qescription
        else:
            return html_diff(markdown.markdown(self.old_value), markdown.markdown(self.new_value))

    def __str__(self):
        return "%s update history" % self.question.title

    class Meta(object):
        ordering = ['-created']
        verbose_name = verbose_name_plural = '问题修改记录'


@python_2_unicode_compatible
class Answer(models.Model):
    body = models.TextField("问题补充", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='创建的用户')
    question = models.ForeignKey(Question, verbose_name='问题')
    created = CreationDateTimeField("创建的时间")

    def get_markdown(self):
        return markdown.markdown(self.body)

    def get_absolute_url(self):
        return reverse("question:answer", kwargs={"pk": self.id})

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if created:
            instance.question.update_status()
            # TODO 添加通知
            from apps.account.models import Focus
            sender = get_model(settings.AUTH_USER_MODEL).objects.get(id=settings.NOTIFICATION_USER)

            notify.send(sender,
                        recipient=instance.question.user,
                        verb=u'你发起的问题[{question}]有新的回答'.format(question=instance.question.title),
                        action_object=instance,
                        description=instance.get_markdown()
            )

            for focus in Focus.get_focus_by_content_object(instance.question).exclude(
                    user__in=[instance.user.id, instance.question.user.id]):
                notify.send(sender,
                            recipient=focus.user,
                            verb=u'你关注的问题[{question}]有新的回答'.format(question=instance.question.title),
                            action_object=instance,
                            description=instance.get_markdown()
                )

    def summary(self, size=30):
        return summary(self.get_markdown(), size)

    def __str__(self):
        return self.question.title

    class Meta(object):
        verbose_name = verbose_name_plural = '回答'


post_save.connect(Answer.post_save, sender=Answer)