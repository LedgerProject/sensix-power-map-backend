from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.geo import choices
from apps.geo.models import GeohashArea


class GeohashAreaListSerializer(serializers.ModelSerializer):
    r = serializers.SerializerMethodField(help_text='Time range key')
    cid = serializers.SerializerMethodField(help_text='Category Id')
    h = serializers.CharField(source='geohash', help_text='Geohash string')
    sid = serializers.SerializerMethodField(help_text='Status Id')

    _time_range_key = None
    _category_id = None

    class Meta:
        model = GeohashArea
        fields = [
            'r', 'cid', 'h', 'sid'
        ]

    def get_r(self, obj) -> str:
        return self._get_time_range_key()

    def get_cid(self, obj) -> str:
        return self._get_category_id()

    def get_sid(self, obj) -> int:
        time_range_key = self._get_time_range_key()
        category_id = self._get_category_id()
        return obj.summary.get(time_range_key, {}).get(category_id, {}).get('sid', choices.STATUS_NONE_ID)

    def _get_time_range_key(self) -> str:
        if self._time_range_key:
            return self._time_range_key

        request = self.context.get('request')

        self._time_range_key = settings.MOVING_AVERAGE_DEFAULT_KEY

        if request:
            self._time_range_key = request.query_params.get('relative_time_range', settings.MOVING_AVERAGE_DEFAULT_KEY)

        if self._time_range_key not in settings.MOVING_AVERAGE_OPTIONS.keys():
            raise ValidationError(detail='Invalid relative time range')

        return self._time_range_key

    def _get_category_id(self) -> str:
        if self._category_id:
            return self._category_id

        request = self.context.get('request')

        self._category_id = choices.CATEGORY_POWER_QUALITY_ID

        if request:
            self._category_id = request.query_params.get('category_id', choices.CATEGORY_POWER_QUALITY_ID)

        if self._category_id not in dict(choices.CATEGORY_ID_CHOICES).keys():
            raise ValidationError(detail='Invalid category Id')

        return self._category_id


class GeohashAreaDetailSerializer(GeohashAreaListSerializer):
    metadata = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    class Meta:
        model = GeohashArea
        fields = GeohashAreaListSerializer.Meta.fields + [
            'data', 'metadata'
        ]

    def get_data(self, obj) -> dict:
        time_range_key = self._get_time_range_key()
        category_id = self._get_category_id()

        return obj.summary.get(time_range_key, {}).get(category_id, {})

    def get_metadata(self, obj) -> dict:
        category_id = self._get_category_id()
        metric_keys = settings.CATEGORY_METRIC_KEYS_MAP.get(category_id, [])

        return {
            metric_key: metadata
            for metric_key, metadata in obj.metadata.items() if metric_key in metric_keys
        }
