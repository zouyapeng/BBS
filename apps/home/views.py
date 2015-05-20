# -*- coding: utf-8 -*-
from django import http
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.shortcuts import render
from django.views import generic
from jieba import posseg
from apps.home.models import Search


class SearchView(generic.ListView):
    model = Search
    template_name = "home/search.html"
    kw = []

    def get_queryset(self):
        words = posseg.cut(self.request.GET['q'])
        self.kw = [self.request.GET['q']]+[k.word for k in words if k.flag in ['n', 'eng'] and len(k.word) > 1]
        if self.kw:
            _re = r'(%s)' % ('|'.join(self.kw))
            return super(SearchView, self).get_queryset().filter(Q(title__regex=_re)|Q(body__regex=_re))

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)

        context['wd_list'] = self.kw
        return context


class HomeView(generic.TemplateView):
    template_name = "home/home.html"

    def get(self, request, *args, **kwargs):
        return http.HttpResponsePermanentRedirect(reverse('article:list'))


