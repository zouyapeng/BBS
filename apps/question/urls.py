from django.conf.urls import include, url
from tastypie.api import NamespacedApi, Api
from apps.question import views
from apps.question.resource import QuestionResource, AnswerResource

api = Api('question')
api.register(QuestionResource())
api.register(AnswerResource())


urlpatterns = [
    # url(r'^api/', include(api.urls)),
    url(r'^(?P<pk>\d+)/history/$', views.HistoryDetailView.as_view(), name='history'),
    url(r'^answer/(?P<pk>\d+)/$', views.AnswerDetailView.as_view(), name='answer'),
    url(r'^(?P<pk>\d+)/$', views.QuestionDetailView.as_view(), name='detail'),
    url(r'^ask/(?P<pk>\d+)/$', views.AskView.as_view(), name='edit'),
    url(r'^ask/$', views.AskView.as_view(), name='ask'),
    url(r'^$', views.QuestionListView.as_view(), name='list'),
]
