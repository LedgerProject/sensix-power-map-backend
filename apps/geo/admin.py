from django.conf import settings
from django.contrib import admin
from django.contrib.admin import register
from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget

from apps.geo import choices
from apps.geo.models import GeohashArea, Metric


@register(GeohashArea)
class GeohashAreaAdmin(admin.ModelAdmin):
    list_display = [
        'geohash',
    ]

    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget()},
    }

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)

        for opt_key, opt_val in settings.MOVING_AVERAGE_OPTIONS.items():
            self._make_thd_v_method_for(opt_key)
            self._make_thd_i_method_for(opt_key)
            self._make_status_method_for(opt_key)

    def _make_thd_v_method_for(self, opt_key):
        def get_thd_v(self, obj):
            return self._get_thd_volgate(obj, opt_key)

        get_thd_v.__name__ = f'{opt_key}_THD_V'
        setattr(self.__class__, get_thd_v.__name__, get_thd_v)
        self.list_display.append(get_thd_v.__name__)

    def _make_thd_i_method_for(self, opt_key):
        def get_thd_i(self, obj):
            return self._get_thd_current(obj, opt_key)

        get_thd_i.__name__ = f'{opt_key}_THD_I'
        setattr(self.__class__, get_thd_i.__name__, get_thd_i)
        self.list_display.append(get_thd_i.__name__)

    def _make_status_method_for(self, opt_key):
        def get_status(self, obj):
            return self._get_status_for(obj, opt_key)

        get_status.__name__ = f'{opt_key}_status'
        setattr(self.__class__, get_status.__name__, get_status)
        self.list_display.append(get_status.__name__)

    def _get_status_for(self, obj, time_range_key: str) -> str:
        category_id = choices.CATEGORY_POWER_QUALITY_ID
        status_id = obj.agg_status.get(time_range_key, {}).get(category_id, choices.STATUS_NONE_ID)
        return dict(choices.STATUS_ID_CHOICES).get(status_id)

    def _get_thd_volgate(self, obj, time_range_key: str) -> float:
        category_id = choices.CATEGORY_POWER_QUALITY_ID
        return obj.agg_data.get(time_range_key, {}).get(category_id, {}).get('metrics', {}).get('THV', {}).get('value')

    def _get_thd_current(self, obj, time_range_key: str) -> float:
        category_id = choices.CATEGORY_POWER_QUALITY_ID
        return obj.agg_data.get(time_range_key, {}).get(category_id, {}).get('metrics', {}).get('THI', {}).get('value')


@register(Metric)
class MetricAdmin(admin.ModelAdmin):
    pass
    search_fields = ['key']
