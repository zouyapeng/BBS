# -*- coding: utf-8 -*-
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization

from apps import BaseResource
from apps.forum.models import Forum

class ForumResource(BaseResource):
    class Meta:
        queryset = Forum.objects.all()
        resource_name = 'forum'
        # authentication = SessionAuthentication()
        # authorization = DjangoAuthorization()
        list_allowed_methods = ['post', 'get']
        detail_allowed_methods = []
        always_return_data = True
