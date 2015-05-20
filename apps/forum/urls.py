from django.conf.urls import include, url
from tastypie.api import Api
from apps.forum import views
from apps.forum.resource import ForumResource


api = Api('forum')
api.register(ForumResource())


urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
]
