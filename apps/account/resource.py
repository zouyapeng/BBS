# # -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.contrib.auth import authenticate, login
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from tastypie import http
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie import fields
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.exceptions import Unauthorized, NotFound, BadRequest, ImmediateHttpResponse, ApiFieldError
from tastypie.utils import trailing_slash, dict_strip_unicode_keys
from apps import BaseResource
from apps.account.models import User, Favorite, Focus, Thank, AnswerVote, Accuracy, Invite, Comment
from apps.article.models import Article, Reply
from apps.article.resource import ArticleResource, ReplyResource
from apps.question.models import Answer, Question
from apps.question.resource import AnswerResource, QuestionResource
from apps.tag.models import Tag
from apps.tag.resource import TagResource


class UserResource(BaseResource):
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/password%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('update_password'), name='password'),
            url(r"^(?P<resource_name>%s)/login%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('login'), name='login_api'),
            url(r"^(?P<resource_name>%s)/username%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('search_username'), name='username_api'),
        ]

    def search_username(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)

        return self.create_response(request, list(
            User.objects.filter(username__icontains=request.GET['q']).values('username')[0:10]))

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        try:
            User.objects.get_by_natural_key(data['username'])
        except:
            return self.create_response(request, {"status": False, 'fields': [{"name": 'username', "msg": '用户名不存在'}]})

        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            if data.get('remember_me'):
                request.session.set_expiry(settings.USERENA_REMEMBER_ME_DAYS)
            else:
                request.session.set_expiry(0)
            next = request.GET.get('next', user.get_absolute_url())
            return self.create_response(request, {"status": True, 'url': next})
        else:
            return self.create_response(request, {"status": False, 'fields': [{"name": 'password', "msg": '密码错误'}]})

    def authorized_update_detail(self, object_list, bundle):
        if bundle.obj != bundle.request.user:
            raise Unauthorized()

    def hydrate_username(self, bundle):
        if bundle.data.has_key("username"):
            del bundle.data["username"]
        return bundle

    # def get_object_list(self, request):
    #     return super(UserResource, self).get_object_list(request).filter(id=request.user.id)

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        return super(UserResource, self).obj_update(bundle, skip_errors, **kwargs)

    def update_password(self, request, **kwargs):
        self.method_check(request, allowed=['put'])
        self.is_authenticated(request)
        user = request.user
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        if deserialized['password'] != deserialized['re_password']:
            return self.create_response(request,
                                        {"status": False, "msg": "新的密码和确认密码不一致"})

        if user.check_password(deserialized.get("old_password")):
            user.set_password(deserialized['password'])
            user.save()
            user = authenticate(username=user.username, password=deserialized['password'])
            login(request, user)
            return self.create_response(request,
                                        {"status": True})
        else:
            return self.create_response(request,
                                        {"status": False, "msg": "原始登陆密码错误"})

    class Meta:
        fields = ['id', 'username', 'email', 'avatar', 'sex', 'birthday', 'signature', 'qq']
        queryset = User.objects.all()
        resource_name = 'user'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post','get']
        detail_allowed_methods = ['put']
        always_return_data = True
        include_absolute_url = True


class InviteResource(BaseResource):
    recipient = fields.ForeignKey(UserResource, attribute='recipient')
    content_object = GenericForeignKeyField({
                                                Question: QuestionResource
                                            }, 'content_object')

    def hydrate_recipient(self, bundle):
        recipient = bundle.data['recipient']
        try:
            if bundle.request.user.username == recipient:
                raise ApiFieldError("不能邀请自己")

            user = User.objects.get_by_natural_key(recipient)
            bundle.data['recipient'] = user
        except ObjectDoesNotExist:
            raise ApiFieldError("用户不存在")
        return bundle

    def save(self, bundle, skip_errors=False):
        obj = self.content_object.hydrate(bundle).obj
        if Invite.objects.filter(recipient=self.recipient.hydrate(bundle).obj, content_type=ContentType.objects.get_for_model(obj), object_id=obj.id).exists():
            raise ApiFieldError("用户邀请")

        return super(InviteResource, self).save(bundle, skip_errors)

    def obj_create(self, bundle, **kwargs):
        return super(InviteResource, self).obj_create(bundle, sender=bundle.request.user)

    class Meta:
        queryset = Invite.objects.all()
        resource_name = 'invite'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True


class FavoriteResource(BaseResource):
    content_object = GenericForeignKeyField({
                                                Answer: AnswerResource,
                                                Article: ArticleResource,
                                                Question: QuestionResource
                                            }, 'content_object')


    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        content_object = self.content_object.hydrate(bundle).obj
        obj = Favorite.objects.filter(user=bundle.request.user,
                                      content_type=ContentType.objects.get_for_model(content_object),
                                      object_id=content_object.id)
        if obj.exists():
            bundle = self.full_bundle(obj[0], bundle.request)
            super(FavoriteResource, self).obj_delete(bundle, **kwargs)
            return http.HttpNoContent()
        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)


    def obj_create(self, bundle, **kwargs):
        return super(FavoriteResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta:
        queryset = Favorite.objects.all()
        resource_name = 'favorite'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True


class FocusResource(BaseResource):
    content_object = GenericForeignKeyField({
                                                Question: QuestionResource,
                                                Article: ArticleResource,
                                                Tag: TagResource,
                                                User: UserResource,
                                            }, 'content_object')


    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        content_object = self.content_object.hydrate(bundle).obj
        obj = Focus.objects.filter(user=bundle.request.user,
                                   content_type=ContentType.objects.get_for_model(content_object),
                                   object_id=content_object.id)
        if obj.exists():
            bundle = self.full_bundle(obj[0], bundle.request)
            super(FocusResource, self).obj_delete(bundle, **kwargs)
            return http.HttpNoContent()
        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)


    def obj_create(self, bundle, **kwargs):
        return super(FocusResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta:
        queryset = Focus.objects.all()
        resource_name = 'focus'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True


class ThankResource(BaseResource):
    content_object = GenericForeignKeyField({
                                                Answer: AnswerResource
                                            }, 'content_object')

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        content_object = self.content_object.hydrate(bundle).obj
        obj = Thank.objects.filter(user=bundle.request.user,
                                   content_type=ContentType.objects.get_for_model(content_object),
                                   object_id=content_object.id)
        if obj.exists():
            bundle = self.full_bundle(obj[0], bundle.request)
            super(ThankResource, self).obj_delete(bundle, **kwargs)
            return http.HttpNoContent()
        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)

    def obj_create(self, bundle, **kwargs):
        return super(ThankResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta:
        queryset = Thank.objects.all()
        resource_name = 'thank'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True


class AccuracyResource(BaseResource):
    content_object = GenericForeignKeyField({
                                                Answer: AnswerResource
                                            }, 'content_object')

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        content_object = self.content_object.hydrate(bundle).obj
        obj = Accuracy.objects.filter(user=bundle.request.user,
                                      content_type=ContentType.objects.get_for_model(content_object),
                                      object_id=content_object.id)
        if obj.exists():
            bundle = self.full_bundle(obj[0], bundle.request)
            super(AccuracyResource, self).obj_delete(bundle, **kwargs)
            return http.HttpNoContent()
        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)

    def obj_create(self, bundle, **kwargs):
        return super(AccuracyResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta:
        queryset = Accuracy.objects.all()
        resource_name = 'accuracy'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True


class AnswerVoteResource(BaseResource):
    content_object = GenericForeignKeyField({
                                                Answer: AnswerResource,
                                                Article: ArticleResource
                                            }, 'content_object')

    def post_list(self, request, **kwargs):
        deserialized = self.deserialize(request, request.body,
                                        format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        content_object = self.content_object.hydrate(bundle).obj
        agree = deserialized['agree']

        obj = AnswerVote.objects.filter(user=bundle.request.user,
                                        content_type=ContentType.objects.get_for_model(content_object),
                                        object_id=content_object.id)

        if obj.exists():
            obj = obj[0]
            if obj.agree == agree:
                bundle = self.full_bundle(obj, bundle.request)
                super(AnswerVoteResource, self).obj_delete(bundle, **kwargs)
                return http.HttpNoContent()
            else:
                bundle.obj = obj
                updated_bundle = self.obj_update(bundle, **self.remove_api_resource_names(kwargs))
        else:
            updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        # bundle = self.full_bundle(obj[0], bundle.request)
        # super(ThankResource, self).obj_delete(bundle, **kwargs)
        # return http.HttpNoContent()
        # updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        # location = self.get_resource_uri(updated_bundle)
        #
        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)

    def obj_create(self, bundle, **kwargs):
        return super(AnswerVoteResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta:
        queryset = AnswerVote.objects.all()
        resource_name = 'vote'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True


class CommentResource(BaseResource):
    user = fields.ForeignKey(UserResource, attribute='user', full=True)

    def build_filters(self, filters=None):
        if filters is None:
            filters = {}
        orm_filters = super(CommentResource, self).build_filters(filters)
        q_set = Q()
        if filters.has_key("content_type"):
            q_set = Q(q_set&Q(content_type=filters['content_type']))

        orm_filters.update({'custom': q_set})
        return orm_filters

    content_object = GenericForeignKeyField({
                                                Question: QuestionResource,
                                                Answer: AnswerResource,
                                                Article: ArticleResource,
                                                Reply: ReplyResource,
                                            }, 'content_object')

    def obj_create(self, bundle, **kwargs):
        return super(CommentResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta:
        queryset = Comment.objects.all()
        resource_name = 'comment'
        # authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        list_allowed_methods = ['post', 'get']
        detail_allowed_methods = []
        always_return_data = True
        filtering = {
            'object_id': ALL,
            'content_type': ALL,
        }