from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from tastypie.api import Api
from apps.question import urls as question_urls
from apps.tag import urls as tag_urls
from apps.attachments import urls as attachment_urls
from apps.account import urls as account_urls
from apps.article import urls as article_urls
from apps.notifications import urls as notifications_urls


urlpatterns = [
    url(r'^account/', include('apps.account.urls', namespace="account")),
    # url(r'^question/', include('apps.question.urls', namespace="question")),
    url(r'^district/', include('apps.district.urls', namespace="district")),
    # url(r'^tag/', include('apps.tag.urls', namespace="tag")),
    url(r'^article/', include('apps.article.urls', namespace="article")),
    url('^notifications/', include('apps.notifications.urls', namespace="notifications")),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(question_urls.api.urls+tag_urls.api.urls+attachment_urls.api.urls
                          +account_urls.api.urls
                          +article_urls.api.urls
                          +notifications_urls.api.urls
                          )),
    url(r'^', include('apps.home.urls', namespace="home")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
