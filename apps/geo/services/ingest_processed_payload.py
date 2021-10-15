import logging
import time
from collections import defaultdict

import geohash
from django.conf import settings

from apps.geo import choices
from apps.geo.models import GeohashArea
from apps.geo.services.moving_average import MovingAverageService

logger = logging.getLogger(__name__)


class IngestProcessedPayloadService(object):
    GEOHASH_PRECISION = 4
    ELIGIBLE_METRIC_KEYS = ['V1r', 'V2r', 'V3r', 'PF1i', 'PF2i', 'PF3i']

    def __init__(self, data: dict, device_metrics: dict, **kwargs) -> None:
        self.device_eui = data['eui']
        self.device_type = data['type']
        self.position = data['position']
        self.payload = data['payload']
        self.latitude = self.position.get('lat')
        self.longitude = self.position.get('lon')
        self.device_metrics = device_metrics
        self.kwargs = kwargs

    def ingest(self):
        start = time.process_time()

        if not self._has_geo_coordinates():
            logger.debug(f'Missing geo coordinates for device {self.device_eui}. ')
            return

        h = geohash.encode(self.latitude, self.longitude, self.GEOHASH_PRECISION)
        area, _ = GeohashArea.objects.get_or_create(geohash=h)

        self._update_area(area)

        area.save(update_fields=['status', 'data'])

        end = time.process_time()
        logger.info(
            f'Ingested processed payload from device {self.device_eui} to geohash "{h}". '
            f'Took: {end - start}s'
        )
        logger.debug(f'Payload: {self.payload}')

    def _update_area(self, area: GeohashArea) -> None:
        updated_data_map = defaultdict(dict)
        updated_status_map = defaultdict(dict)

        for metric_key, value in self._get_payload_data().items():
            for opt_key, opt_val in settings.MOVING_AVERAGE_OPTIONS.items():
                current_data = area.data.get(opt_key, {})

                updated_data = self._compute_data_for(value, opt_val, current_data)
                updated_last_value = updated_data.get('agg', {}).get('lv')

                updated_status = self._compute_status_for(updated_last_value, metric_key)

                updated_data_map[opt_key][metric_key] = updated_data
                updated_status_map[opt_key][metric_key] = updated_status

        area.data = updated_data_map
        area.status = updated_status_map

    def _has_geo_coordinates(self) -> bool:
        return self.latitude is not None and self.longitude is not None

    def _get_payload_data(self) -> dict:
        return {
            k: v for k, v in self.payload.get('data', {}).items() if k in self.ELIGIBLE_METRIC_KEYS
        }

    def _compute_data_for(self, value: float, opt_val: dict, current_data: dict) -> dict:
        return MovingAverageService(
            relative_time_range=opt_val.get('range'),
            window_size=opt_val.get('window'),
            precision=2
        ).update(value, self.payload.get('timestamp'), current_data)

    def _compute_status_for(self, value: float, metric_key: str) -> dict:
        updated_status = {
            'sid': choices.STATUS_NONE_ID,
        }

        status_keys_map = {
            'c': choices.STATUS_CRITICAL_ID,
            'w': choices.STATUS_WARNING_ID,
            'n': choices.STATUS_NORMAL_ID,
        }

        metric = self.device_metrics.get(metric_key)
        thresholds = metric.get('thresholds', {})

        for status_key in status_keys_map.keys():
            for threshold in thresholds.get(status_key, []):
                x1 = threshold.get('x1')
                x2 = threshold.get('x2')

                if x1 <= value <= x2:
                    updated_status['sid'] = status_keys_map.get(status_key)
                    updated_status['l'] = threshold.get('l')

                    return updated_status

        return updated_status
