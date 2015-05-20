from django.conf.urls import include, url
from tastypie.api import Api
from apps.account import views
from apps.account.resource import UserResource, FavoriteResource, FocusResource, ThankResource, AnswerVoteResource, \
    AccuracyResource, InviteResource, CommentResource

api = Api('account')
api.register(UserResource())
api.register(FavoriteResource())
api.register(FocusResource())
api.register(ThankResource())
api.register(AccuracyResource())
api.register(AnswerVoteResource())
api.register(InviteResource())
api.register(CommentResource())

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^register/$', views.RegisterView.as_view(), name='register'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.Logout, name='logout'),
    url(r'^casuserget/$', 'apps.account.views.cas_get', name='casget'),
    url(r'^cas/$', 'apps.account.views.caslogin',name='cas'),
    url(r'^favorite/$', views.FavoriteView.as_view(), name='favorite'),
    url(r'^invite/$', views.InviteView.as_view(), name='invite'),
    url(r'^setting/(?P<tag>.+)/$', views.SettingView.as_view(), name='setting'),
    url(r'^user/(?P<name>.+)/(?P<tag>.+)/$', views.UserDetailView.as_view(), name='detail_tag'),
    url(r'^user/(?P<name>.+)/$', views.UserDetailView.as_view(), name='detail'),
]
