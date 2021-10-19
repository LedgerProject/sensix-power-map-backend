from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.geo import choices
from apps.geo.models import GeohashArea


class GeohashAreaListSerializer(serializers.ModelSerializer):
    r = serializers.SerializerMethodField()
    summary = serializers.SerializerMethodField()

    _time_range_key = None

    class Meta:
        model = GeohashArea
        fields = [
            'geohash', 'summary', 'r'
        ]

    def get_r(self, obj):
        return self._get_time_range_key()

    def get_summary(self, obj):
        request = self.context.get('request')
        category_id = request.query_params.get('category_id', choices.CATEGORY_POWER_QUALITY_ID)
        return obj.status.get(category_id, {})

    def _get_time_range_key(self):
        if self._time_range_key:
            return self._time_range_key

        request = self.context.get('request')

        self._time_range_key = settings.MOVING_AVERAGE_DEFAULT_KEY

        if request:
            self._time_range_key = request.query_params.get('relative_time_range', settings.MOVING_AVERAGE_DEFAULT_KEY)

        if self._time_range_key not in settings.MOVING_AVERAGE_OPTIONS.keys():
            raise ValidationError(detail='Invalid relative time range')

        return self._time_range_key


class GeohashAreaDetailSerializer(GeohashAreaListSerializer):
    status = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = GeohashArea
        fields = GeohashAreaListSerializer.Meta.fields + [
            'status', 'data'
        ]

    def get_status(self, obj):
        key = self._get_time_range_key()
        return obj.status.get(key, {})

    def get_data(self, obj) -> dict:
        key = self._get_time_range_key()
        return obj.data.get(key, {})
