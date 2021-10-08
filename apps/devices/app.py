from django.apps import AppConfig


class DevicesAppConfig(AppConfig):
    name = 'apps.devices'
    verbose_name = 'Devices'

    def ready(self):
        pass
