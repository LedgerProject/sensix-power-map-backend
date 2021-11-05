import json

from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from apps.geo import choices
from apps.geo.models import GeohashArea


class GeohashAreaListSerializer(serializers.ModelSerializer):
    h = serializers.CharField(help_text='Geohash string')
    sid = serializers.IntegerField(help_text='Status Id')

    class Meta:
        model = GeohashArea
        fields = [
            'h', 'sid'
        ]


class GeohashAreaDetailSerializer(GeohashAreaListSerializer):
    metadata = serializers.SerializerMethodField()
    data = serializers.SerializerMethodField()

    _category_id = None

    class Meta:
        model = GeohashArea
        fields = GeohashAreaListSerializer.Meta.fields + [
            'data', 'metadata'
        ]

    def get_data(self, obj) -> dict:
        return json.loads(obj.agg_data_subset)

    def get_metadata(self, obj) -> dict:
        category_id = self._get_category_id()
        metric_keys = settings.CATEGORY_METRIC_KEYS_MAP.get(category_id, [])

        metadata = {
            metric_key: metadata
            for metric_key, metadata in obj.metadata.items()
            if metric_key in metric_keys if metric_key not in settings.THD_METRIC_KEYS
        }

        metadata.update({
            settings.THD_AGG_VOLTAGE_METRIC_KEY: {
                **obj.metadata.get(settings.THD_VOLTAGE_METRIC_KEYS[0], {}),
                'name': 'Voltage THD',
                'short_name': 'THD V'
            },
            settings.THD_AGG_CURRENT_METRIC_KEY: {
                **obj.metadata.get(settings.THD_CURRENT_METRIC_KEYS[0], {}),
                'name': 'Current THD',
                'short_name': 'THD I'
            }
        })

        return metadata

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
