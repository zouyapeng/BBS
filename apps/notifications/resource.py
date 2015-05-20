# # -*- coding: utf-8 -*-
from tastypie.authorization import DjangoAuthorization
from apps import BaseResource
from apps.notifications.models import Notification


class NotificationResource(BaseResource):

    def get_object_list(self, request):
        return super(NotificationResource, self).get_object_list(request).filter(recipient=request.user)

    class Meta:
        queryset = Notification.objects.all()
        resource_name = 'notification'
        authorization = DjangoAuthorization()
        detail_allowed_methods = ['put']
