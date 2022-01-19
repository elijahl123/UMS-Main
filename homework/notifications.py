from base.decorators import register_class
from base.notifications import NotificationsConfig


@register_class()
class HomeworkNotifications(NotificationsConfig):
    template = 'email/'
