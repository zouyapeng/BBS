from django.conf.urls import include, url
from tastypie.api import Api
from apps.article import views
from apps.article.resource import ForumResource, ArticleResource, ReplyResource

api = Api('article')
api.register(ForumResource())
api.register(ArticleResource())
api.register(ReplyResource())

urlpatterns = [
    url(r'^$', views.ArticleListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.ArticleDetailView.as_view(), name='detail'),
    url(r'^reply/(?P<pk>\d+)/$', views.ReplyDetailView.as_view(), name='reply'),
    url(r'^(?P<pk>\d+)/history/$', views.ArticleDetailView.as_view(), name='history'),
    url(r'^new/(?P<pk>\d+)/$', views.ArticleNewView.as_view(), name='edit'),
    url(r'^new/$', views.ArticleNewView.as_view(), name='new'),
]
