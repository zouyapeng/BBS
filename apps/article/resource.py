# # -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.utils.timezone import now
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.exceptions import ApiFieldError, Unauthorized
from tastypie.validation import FormValidation
from apps import BaseResource, CreateTagResource, Tag
from apps.article.models import Forum, Article, Reply
from apps.attachments.models import Attachment


class ForumResource(BaseResource):
    class Meta:
        queryset = Forum.objects.all()
        resource_name = 'forum'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post','get']
        detail_allowed_methods = []
        always_return_data = True


class ArticleResource(BaseResource, CreateTagResource):
    forum = fields.ForeignKey(ForumResource, 'forum', full=True)

    def hydrate_title(self, bundle):
        title = bundle.data.get("title", '')
        if 1 < len(title) < 50:
            return bundle
        raise ApiFieldError("您的文章标题为2~50个字，请精简或将更多内容输入到文章内容中")

    def obj_create(self, bundle, **kwargs):
        user = bundle.request.user
        bundle = super(ArticleResource, self).obj_create(bundle, user=user)
        attachments = bundle.data.get("attachment")
        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]
            Attachment.objects.filter(object_id__isnull=True, id__in=attachments).update(object_id=bundle.obj.id,
                                                                                         content_type=ContentType.objects.get_for_model(
                                                                                             bundle.obj))
        # 标签
        tag_objects = self.set_tag(bundle)
        for tag in tag_objects:
            ArticleTag(article=bundle.obj, tag=tag).save()
        return bundle

    def authorized_update_detail(self, object_list, bundle):
        auth_result = super(ArticleResource, self).authorized_update_detail(object_list, bundle)
        if bundle.request.user != bundle.obj.user:
            self.unauthorized_result(Unauthorized())
        return auth_result


    def obj_update(self, bundle, skip_errors=False, **kwargs):
        bundle = super(ArticleResource, self).obj_update(bundle, skip_errors, **kwargs)
        # 文件
        attachments = bundle.data.get("attachment")
        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]
            Attachment.objects.filter(object_id__isnull=True, id__in=attachments).update(object_id=bundle.obj.id,
                                                                                         content_type=ContentType.objects.get_for_model(
                                                                                             bundle.obj))
            Attachment.objects.filter(object_id=bundle.obj.id,
                                      content_type=ContentType.objects.get_for_model(
                                          bundle.obj),
            ).exclude(id__in=attachments).update(object_id=None, content_type=None)

        # 标签
        tag_objects = self.set_tag(bundle)
        ArticleTag.objects.filter(article=bundle.obj).exclude(tag__in=tag_objects).delete()
        for tag in tag_objects:
            if not bundle.obj.articletag_set.filter(tag=tag).exists():
                ArticleTag(article=bundle.obj, tag=tag).save()

        return bundle

    class Meta:
        queryset = Article.objects.all()
        resource_name = 'article'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post','get']
        detail_allowed_methods = ['put']
        include_absolute_url = True
        always_return_data = True
        excludes = ['kw']


class ReplyResource(BaseResource):
    article = fields.ForeignKey(ArticleResource, 'article', full=True)

    def obj_create(self, bundle, **kwargs):
        bundle = super(ReplyResource, self).obj_create(bundle, user=bundle.request.user)

        attachments = bundle.data.get("attachment")
        if attachments:
            if not isinstance(attachments, list):
                attachments = [attachments]
            Attachment.objects.filter(object_id__isnull=True,
                                      id__in=attachments).update(object_id=bundle.obj.id,
                                                                 content_type=ContentType.objects.get_for_model(bundle.obj))
        return bundle

    class Meta:
        queryset = Reply.objects.all()
        resource_name = 'reply'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True
