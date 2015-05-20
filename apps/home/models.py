# -*- coding: utf-8 -*-
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Search(models.Model):
    '''
    CREATE  VIEW   home_search AS
    SELECT django_content_type.id||article_article.id as id, article_article.id as object_id, django_content_type.id as content_type_id, article_article.title as title, article_article.body as body FROM article_article left  join django_content_type on django_content_type.model = 'article' and django_content_type.app_label = 'article'
  UNION
SELECT  django_content_type.id || question_question.id as id, question_question.id as object_id, django_content_type.id as content_type_id, question_question.title as title, question_question.body as body from question_question left  join django_content_type on django_content_type.model = 'question' and django_content_type.app_label = 'question'
 UNION
SELECT django_content_type.id || tag_tag.id as id, tag_tag.id as object_id, django_content_type.id as content_type_id, tag_tag.title as title, tag_tag.describe as body FROM tag_tag left  join django_content_type on django_content_type.model = 'tag' and django_content_type.app_label = 'tag'
UNION
SELECT django_content_type.id || account_user.id as id, account_user.id as object_id, django_content_type.id as content_type_id, account_user.username as title, account_user.signature as body FROM account_user left  join django_content_type on django_content_type.model = 'user' and django_content_type.app_label = 'account'
UNION
SELECT django_content_type.id || article_reply.id as id, article_reply.id as object_id, django_content_type.id as content_type_id, article_reply.body as body, null as title FROM article_reply left  join django_content_type on django_content_type.model = 'reply' and django_content_type.app_label = 'article'
UNION
SELECT django_content_type.id || question_answer.id as id, question_answer.id as object_id, django_content_type.id as content_type_id, question_answer.body as body, null as title FROM question_answer left  join django_content_type on django_content_type.model = 'answer' and django_content_type.app_label = 'question'
    '''
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    body = models.TextField()
    title = models.CharField(max_length=255)

    class Meta(object):
        managed = False
        verbose_name = verbose_name_plural = '搜索'