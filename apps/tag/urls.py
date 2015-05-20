from django.conf.urls import include, url
from tastypie.api import Api
from apps.tag import views
from apps.tag.resource import TagResource


api = Api('tag')
api.register(TagResource())

urlpatterns = [
    url(r'^$', views.TagListView.as_view(), name='tag_list'),
    # url(r'^api/', include(api.urls)),
    url(r'^(?P<title>.+)/$', views.TagDetailView.as_view(), name='tag_detail'),
]
