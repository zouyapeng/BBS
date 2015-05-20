# -*- coding: utf-8 -*-
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization

from apps import BaseResource
from apps.district.models import District

class DistrictResource(BaseResource):
    class Meta:
        queryset = District.objects.all()
        resource_name = 'district'
        # authentication = SessionAuthentication()
        # authorization = DjangoAuthorization()
        list_allowed_methods = ['post', 'get']
        detail_allowed_methods = []
        always_return_data = True
