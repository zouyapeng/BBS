from django.conf import settings
from apps.notifications.models import Notification


def config(request):
    content = {
        'DEFAULT_PAGINATION': settings.DEFAULT_PAGINATION,
        'PATH': filter(lambda x: x, request.path.split('/')),
    }
    if request.user.is_authenticated():
        content.update({
            "notifications_unread_count": request.user.notifications.filter(unread=True).count(),
            "notifications_unread": request.user.notifications.filter(unread=True)[:5]
        })


    return content

