from django.apps import AppConfig


class CoreAppConfig(AppConfig):
    name = 'apps.core'
    verbose_name = 'Core'

    def ready(self):
        try:
            from apps.core import signals
            from apps.core import exceptions
        except ImportError as e:
            raise e
