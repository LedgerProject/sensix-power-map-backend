from django.contrib import admin
from django.contrib.admin import register
from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget

from apps.geo import choices
from apps.geo.models import GeohashArea


@register(GeohashArea)
class GeohashAreaAdmin(admin.ModelAdmin):
    list_display = ['geohash', 'status_r3', 'status_r8', 'status_r24', 'status_r48']
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget()},
    }

    def status_r3(self, obj):
        return self._get_status_for(obj, 'r3')

    def status_r8(self, obj):
        return self._get_status_for(obj, 'r8')

    def status_r24(self, obj):
        return self._get_status_for(obj, 'r24')

    def status_r48(self, obj):
        return self._get_status_for(obj, 'r48')

    def _get_status_for(self, obj, time_range_key: str) -> int:
        category_id = str(choices.CATEGORY_POWER_QUALITY_ID)
        return obj.summary.get(time_range_key, {}).get(category_id, {}).get('sid')
