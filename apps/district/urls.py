from django.conf.urls import include, url
from tastypie.api import Api
from apps.district import views
from apps.district.resource import DistrictResource


api = Api('district')
api.register(DistrictResource())

urlpatterns = [
    url(r'^$', views.HomeView, name='list'),
]
