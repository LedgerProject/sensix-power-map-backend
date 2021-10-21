from django.contrib import admin
from django.contrib.admin import register
from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget

from apps.geo import choices
from apps.geo.models import GeohashArea, Metric


@register(GeohashArea)
class GeohashAreaAdmin(admin.ModelAdmin):
    list_display = ['geohash', 'status_r3', 'status_r8', 'status_r24', 'status_r48']
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget()},
    }

    def status_r3(self, obj):
        status_id = self._get_status_for(obj, 'r3')
        return dict(choices.STATUS_ID_CHOICES).get(status_id)

    def status_r8(self, obj):
        status_id = self._get_status_for(obj, 'r8')
        return dict(choices.STATUS_ID_CHOICES).get(status_id)

    def status_r24(self, obj):
        status_id = self._get_status_for(obj, 'r24')
        return dict(choices.STATUS_ID_CHOICES).get(status_id)

    def status_r48(self, obj):
        status_id = self._get_status_for(obj, 'r48')
        return dict(choices.STATUS_ID_CHOICES).get(status_id)

    def _get_status_for(self, obj, time_range_key: str) -> int:
        category_id = choices.CATEGORY_POWER_QUALITY_ID
        return obj.agg_status.get(time_range_key, {}).get(category_id, choices.STATUS_NONE_ID)


@register(Metric)
class MetricAdmin(admin.ModelAdmin):
    pass
    search_fields = ['key']
