# coding: utf-8
from difflib import SequenceMatcher
import json
import re
import urllib
import urllib2
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import generic
import markdown
import math
from simplediff import html_diff
from apps import RedirectToLoginMixin
from apps.account.models import History, Invite
from apps.article.models import Article, Reply
from apps.notifications.models import Notification
from apps.question.models import Question, Answer
from apps.tag.models import Tag
from jieba import posseg


class QuestionDetailView(generic.DetailView):
    model = Question
    template_name = "question/detail.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        History.generate_history(self.object, self.request)

        if self.object.kw:
            words = [self.object.title] + self.object.kw
            _re = r'(%s)' % ('|'.join(words))
            related_question = Question.objects.filter(Q(body__regex=_re) | Q(title__regex=_re)).exclude(
                id=self.object.id)[:20]
            context['related_question'] = related_question
        context['invites'] = Invite.objects.filter(content_type=ContentType.objects.get_for_model(self.object), object_id=self.object.id)
        return context


class AnswerDetailView(generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        obj = Answer.objects.get(id=kwargs['pk'])
        count = obj.question.answer_set.filter(created__lt=obj.created).count() + 1
        page = int(math.ceil(count / float(settings.DEFAULT_PAGINATION.answer)))
        query = {}
        if page != 1:
            query['page'] = page
        for k, v in self.request.GET.items():
            if k == 'notification':
                try:
                    Notification.objects.filter(id=v, unread=True).update(unread=False)
                except:
                    pass
                continue
            query[k] = v
        return "{url}?{query}#answer-{pk}".format(url=reverse("question:detail",
                                                              kwargs={"pk": obj.question.id}),
                                                  query=urllib.urlencode(query),
                                                  pk=kwargs['pk']
        )


class HistoryDetailView(QuestionDetailView):
    model = Question
    template_name = "question/history.html"

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        if self.object.kw:
            words = [self.object.title] + self.object.kw
            _re = r'(%s)' % ('|'.join(words))
            related_question = Question.objects.filter(Q(body__regex=_re) | Q(title__regex=_re)).exclude(
                id=self.object.id)[:20]
            context['related_question'] = related_question
        context['questionhistory_set'] = context['question'].questionhistory_set.all().select_related("user")

        return context


class QuestionListView(generic.ListView):
    model = Question
    template_name = "question/list.html"
    ordering = '-created'

    def get_ordering(self):
        if self.request.GET.get("order_by") == 'unresponsive':
            return 'last_answer_date'
        elif self.request.GET.get("order_by") == 'hot':
            return '-answer_count'
        return super(QuestionListView, self).get_ordering()

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        context['new_answers'] = Answer.objects.all().order_by('-created')[:10]

        from django.db import connection, transaction
        cursor = connection.cursor()
        cursor.execute('SELECT count(tag_id) as c, tag_id, title from ( SELECT question_questiontag.tag_id, tag_tag.title FROM question_questiontag left join tag_tag on tag_tag.id=question_questiontag.tag_id union  all SELECT article_articletag.tag_id, tag_tag.title FROM article_articletag left join tag_tag on tag_tag.id=article_articletag.tag_id) group by tag_id order by c desc limit 0, 20')
        context['popular'] = cursor.fetchall()

        return context


class AskView(generic.TemplateView):
    template_name = "question/ask.html"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            if Question.objects.get(id=pk).user != request.user:
                return HttpResponse(status=401)
        return super(AskView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(AskView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(AskView, self).get_context_data(**kwargs)
        if kwargs.get("pk"):
            context['question'] = question = Question.objects.get(id=kwargs.get("pk"))
            context['questionattachment_set'] = question.questionattachment_set.all().select_related("attachment")

        return context

    def get(self, request, *args, **kwargs):
        return super(AskView, self).get(request, *args, **kwargs)
