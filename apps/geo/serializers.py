from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.geo.models import GeohashArea


class GeohashAreaSerializer(serializers.ModelSerializer):
    r = serializers.SerializerMethodField()

    status = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    _time_range_key = None

    class Meta:
        model = GeohashArea
        fields = [
            'geohash', 'status', 'data', 'r'
        ]

    def get_r(self, obj):
        return self._get_time_range_key()

    def get_data(self, obj) -> dict:
        key = self._get_time_range_key()
        return obj.data.get(key, {})

    def get_status(self, obj):
        key = self._get_time_range_key()
        return obj.status.get(key, {})

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
