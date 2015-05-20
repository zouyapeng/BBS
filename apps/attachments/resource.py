# # -*- coding: utf-8 -*-
import json
import re
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.db.models import Q
from tastypie import http
from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from apps import BaseResource
from apps.attachments.models import Attachment


class AttachmentResource(BaseResource):
    def post_list(self, request, **kwargs):
        attachment_file = request.FILES['file']
        upload_file_name = attachment_file.name
        att = Attachment.objects.create(source_filename=upload_file_name, creator=request.user, attachment_file=attachment_file)
        att.save()
        updated_bundle = self.full_bundle(obj=att, request=request)
        location = self.get_resource_uri(updated_bundle)
        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)

    class Meta:
        queryset = Attachment.objects.all()
        resource_name = 'attachment'
        authorization = DjangoAuthorization()
        authentication = SessionAuthentication()
        list_allowed_methods = ['post']
        detail_allowed_methods = []
        always_return_data = True
