# # -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import ApiFieldError
from tastypie.resources import NamespacedModelResource, ModelResource, Resource
from apps.tag.models import Tag


class BaseResource(ModelResource):
    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
        else:
            custom = None
        semi_filtered = super(BaseResource, self).apply_filters(request, applicable_filters)
        return semi_filtered.filter(custom).distinct() if custom else semi_filtered


    @classmethod
    def full_bundle(cls, obj, request=None, full=True):
        self = cls()
        bundle = self.build_bundle(obj=obj, request=request)
        bundle.full = full
        bundle = self.full_dehydrate(bundle)
        return bundle


class CreateTagResource(object):
    def set_tag(self, bundle):
        user = bundle.request.user
        tags = bundle.data.get("tags")
        if not tags:
            raise ApiFieldError("标签错误")
        tags = set(map(lambda tag: tag.strip(), tags.split(",")))

        if len(tags) > 5:
            raise ApiFieldError("标签不能超过5个")

        tag_objects = []
        for tag_name in tags:
            tag_objects.append(Tag.objects.get_or_create(defaults={'user': user}, title=tag_name)[0])
        return tag_objects


class RedirectToLoginMixin(object):
    """ mixin which redirects to settings.LOGIN_URL if the view encounters an PermissionDenied exception
        and the user is not authenticated. Views inheriting from this need to implement
        get_login_redirect_url(), which returns the URL to redirect to after login (parameter "next")
    """
    def dispatch(self, request, *args, **kwargs):
        try:
            return super(RedirectToLoginMixin, self).dispatch(request, *args, **kwargs)
        except PermissionDenied:
            if not request.user.is_authenticated():
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(self.get_login_redirect_url())
            else:
                return HttpResponseForbidden()

    def get_login_redirect_url(self):
        """ get the url to which we redirect after the user logs in. subclasses should override this """
        return '/'