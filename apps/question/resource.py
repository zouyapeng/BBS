# # -*- coding: utf-8 -*-
import json
import re
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.db.models import Q
from tastypie.authorization import DjangoAuthorization
from tastypie.constants import ALL
from tastypie.exceptions import ApiFieldError, ImmediateHttpResponse, Unauthorized
from tastypie.utils import trailing_slash
from apps import BaseResource, CreateTagResource
from apps.attachments.models import Attachment
from apps.question.models import Question, Answer, QuestionTag, QuestionAttachment
from apps.tag.models import Tag
from jieba import posseg
from tastypie import fields


class QuestionResource(BaseResource, CreateTagResource):
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/related%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('related'), name='related'),
        ]

    def related(self, request, **kwargs):
        q = request.GET.get("q")
        if q:
            words = posseg.cut(q)
            words = [q] + [k.word for k in words if k.flag in ['n', 'eng'] and len(k.word) > 1]
            if words:
                _re = r'(%s)' % ('|'.join(words))
                pattern = re.compile(r'(%s)' % '|'.join(words).encode("utf-8"))
                objects = self.get_object_list(request).filter(Q(title__regex=_re))
                paginator = self._meta.paginator_class(request.GET, objects,
                                                       resource_uri=self.get_resource_uri(),
                                                       limit=self._meta.limit,
                                                       max_limit=self._meta.max_limit,
                                                       collection_name=self._meta.collection_name)
                to_be_serialized = paginator.page()
                bundles = []
                for obj in to_be_serialized[self._meta.collection_name]:
                    bundle = self.full_bundle(obj, request)
                    bundle.data['title'] = pattern.sub(r'<span class="color-red">\1</span>',
                                                       bundle.data['title'].encode("utf-8"))
                    bundles.append(bundle)

                to_be_serialized[self._meta.collection_name] = bundles
                to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
                to_be_serialized["kw"] = filter(lambda x:x!=q, words)
                return self.create_response(request, to_be_serialized)
        return self.create_response(request, {"objects": []})

    def obj_create(self, bundle, **kwargs):
        tags = bundle.data.get("tags")
        user = bundle.request.user
        if not tags:
            raise ApiFieldError("标签错误")

        bundle = super(QuestionResource, self).obj_create(bundle, user=user)

        #文件
        attachments = bundle.data.get("attachment")
        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]
            for attachment in attachments:
                qa = QuestionAttachment.objects.get_or_create(question=bundle.obj, attachment_id=int(attachment))[0]

        # 问题标签
        tag_objects = self.set_tag(bundle)
        for t in tag_objects:
            QuestionTag(question=bundle.obj, tag=t).save()

        return bundle

    def authorized_update_detail(self, object_list, bundle):
        auth_result = super(QuestionResource, self).authorized_update_detail(object_list, bundle)
        if bundle.request.user != bundle.obj.user:
            self.unauthorized_result(Unauthorized())

        return auth_result


    def obj_update(self, bundle, skip_errors=False, **kwargs):

        bundle = super(QuestionResource, self).obj_update(bundle, skip_errors, **kwargs)

        #文件
        attachments = bundle.data.get("attachment")
        attachment_ids = []
        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]
            for attachment in attachments:
                qa = QuestionAttachment.objects.get_or_create(question=bundle.obj, attachment_id=int(attachment))[0]
                attachment_ids.append(attachment)
        QuestionAttachment.objects.filter(question=bundle.obj).exclude(attachment_id__in=attachment_ids).delete()
        # 标签
        tag_objects = self.set_tag(bundle)
        QuestionTag.objects.filter(question=bundle.obj).exclude(tag__in=tag_objects).delete()
        for tag in tag_objects:
            if not bundle.obj.questiontag_set.filter(tag=tag).exists():
                QuestionTag(question=bundle.obj, tag=tag).save()

        return bundle

    class Meta:
        queryset = Question.objects.all()
        resource_name = 'question'
        include_absolute_url = True
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = ['put']
        always_return_data = True
        excludes = ['kw']
        filtering = {
            'id': ALL
        }


class AnswerResource(BaseResource):
    question = fields.ForeignKey(QuestionResource, attribute='question')

    def obj_create(self, bundle, **kwargs):
        user = bundle.request.user
        return super(AnswerResource, self).obj_create(bundle, user=user)

    class Meta:
        queryset = Answer.objects.all()
        resource_name = 'answer'
        include_absolute_url = True
        authorization = DjangoAuthorization()
        list_allowed_methods = ['get', 'post']
        detail_allowed_methods = ['get']
        always_return_data = True
        filtering = {
            'id': ALL
        }
