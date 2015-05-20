# # -*- coding: utf-8 -*-
from django.conf.urls import url
from jieba import posseg
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL
from tastypie.utils import trailing_slash
from apps import BaseResource
from apps.tag.models import Tag


class TagResource(BaseResource):

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/related%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('related'), name='related'),
        ]

    def related(self, request, **kwargs):
        q = request.GET.get("q")
        if q:
            words = posseg.cut(q)
            words = [k.word for k in words if k.flag in ['n', 'eng'] and len(k.word) > 1]
            return self.create_response(request, words)

    def dehydrate(self, bundle):
        bundle.data['question_count'] = bundle.obj.question_set.count()
        return bundle

    class Meta:
        queryset = Tag.objects.all()
        resource_name = 'tag'
        authorization = DjangoAuthorization()
        list_allowed_methods = ['get']
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
            "title": ALL
        }
