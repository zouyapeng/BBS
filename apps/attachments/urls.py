from django.conf.urls import include, url
from tastypie.api import Api
from apps.question import views
from apps.attachments.resource import AttachmentResource

api = Api('attachment')
api.register(AttachmentResource())

