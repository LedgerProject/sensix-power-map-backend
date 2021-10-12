from django.apps import AppConfig


class GeoAppConfig(AppConfig):
    name = 'apps.geo'
    verbose_name = 'Geo'

    def ready(self):
        pass
