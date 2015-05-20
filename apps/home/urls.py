from django.conf.urls import include, url
from apps.home import views

urlpatterns = [
    url(r'^search/$', views.SearchView.as_view(), name='search'),
    url(r'^$', views.HomeView.as_view(), name='home'),
]
