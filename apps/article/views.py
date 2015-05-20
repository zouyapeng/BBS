# -*- coding: utf-8 -*-
import urllib
import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import generic
import math
from apps.account.models import User, History
from apps.article.models import Article, Reply
from apps.forum.models import Forum
from apps.notifications.models import Notification


class ArticleListView(generic.ListView):
    model = Article
    template_name = "article/list.html"
    ordering = '-update_date'

    def get_ordering(self):
        if self.request.GET.get("order_by") == '-created':
            return '-created'
        return super(ArticleListView, self).get_ordering()

    def get_queryset(self):
        forum_id = self.request.GET.get('forum')
        object_list = super(ArticleListView, self).get_queryset()
        if forum_id:
            object_list = object_list.filter(forum=forum_id)

        return object_list

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        forums = Forum.objects.all()
        context['forums'] = forums
        forum_id = self.request.GET.get('forum')
        if forum_id:
            context['forum'] = Forum.objects.get(id=forum_id)
            # 今日发帖数
            context['count2'] = self.object_list.filter(forum=context['forum'], created__gt=datetime.datetime(now().year, now().month, now().day)).count()
            #ALL
            context['count1'] = self.object_list.filter(forum=context['forum']).count()
            #昨天
            context['count3'] = self.object_list.filter(forum=context['forum'], created__gt=datetime.datetime(now().year, now().month, now().day)-datetime.timedelta(days=1)).count()
            context['count4'] = Reply.objects.filter(article__forum=context['forum'], created__gt=datetime.datetime(now().year, now().month, now().day)).count()
        else:
            # 今日发帖数
            context['count2'] = self.object_list.filter(created__gt=datetime.datetime(now().year, now().month, now().day)).count()
            #ALL
            context['count1'] = self.object_list.count()
            #昨天
            context['count3'] = self.object_list.filter(created__gt=datetime.datetime(now().year, now().month, now().day)-datetime.timedelta(days=1)).count()
            context['count4'] = Reply.objects.filter(created__gt=datetime.datetime(now().year, now().month, now().day)).count()


        return context


class ReplyDetailView(generic.RedirectView):
    permanent = True

    def get_redirect_url(self, *args, **kwargs):
        obj = Reply.objects.get(id=kwargs['pk'])
        count = obj.article.reply_set.filter(created__lt=obj.created).count() + 1
        page = int(math.ceil(count / float(settings.DEFAULT_PAGINATION.reply)))
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
        return "{url}?{query}#reply-{pk}".format(url=reverse("article:detail",
                                                                 kwargs={"pk": obj.article.id}),
                                                     query=urllib.urlencode(query),
                                                     pk=kwargs['pk']
        )


class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = "article/detail.html"

    def get(self, request, *args, **kwargs):
        response = super(ArticleDetailView, self).get(request, *args, **kwargs)
        History.generate_history(self.object, request)
        return response

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        if self.object.kw:
            words = [self.object.title] + self.object.kw
            _re = r'(%s)' % ('|'.join(words))
            related_article = Article.objects.filter(Q(body__regex=_re) | Q(title__regex=_re)).exclude(
                id=self.object.id)[:20]
            context['related_article'] = related_article

        return context


class ArticleNewView(generic.TemplateView):
    template_name = "article/new.html"

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        if pk:
            if Article.objects.get(id=pk).user != request.user:
                return HttpResponse(status=401)

        return super(ArticleNewView, self).get(request, *args, **kwargs)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ArticleNewView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ArticleNewView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        if pk:
            context['article'] = article = Article.objects.get(id=pk)
            # context['attachments'] = article.questionattachment_set.all().select_related("attachment")
        else:
            forums = Forum.objects.all()
            context['forums'] = forums


        return context