from base.notifications import notifications_framework


def register_class():
    def _model_notification_wrapper(config_class):
        notifications_framework.register(config_class)
        return config_class

    return _model_notification_wrapper