import logging
import time
from collections import defaultdict

import geohash
from django.conf import settings

from apps.geo.cache import MetricDetailCacheJob
from apps.geo.models import GeohashArea, Metric
from apps.geo.services.data_service_class_map import AGGREGATION_SERVICE_CLASS_MAP
from apps.geo.services.moving_average import MovingAverageService
from apps.geo.services.status import StatusService

logger = logging.getLogger(__name__)


class IngestProcessedPayloadService(object):
    GEOHASH_PRECISION = 4
    VALUE_PRECISION = 2

    def __init__(self, data: dict, **kwargs) -> None:
        self.device_eui = data['eui']
        self.device_type = data['type']
        self.position = data['position']
        self.payload = data['payload']
        self.latitude = self.position.get('lat')
        self.longitude = self.position.get('lon')
        self.kwargs = kwargs

    def ingest(self):
        start = time.process_time()

        if self.device_type not in settings.ELIGIBLE_DEVICE_TYPES:
            logger.debug(f'Skipping {self.device_eui}. {self.device_type} is not eligible.')
            return

        if not self._has_geo_coordinates():
            logger.debug(f'Missing geo coordinates for device {self.device_eui}. Abort ingestion.')
            return

        h = geohash.encode(self.latitude, self.longitude, self.GEOHASH_PRECISION)
        area, _ = GeohashArea.objects.get_or_create(geohash=h)

        self._update_area_fields(area)
        self._update_area_summary(area)

        area.save(update_fields=['summary', 'metadata', 'status', 'data'])

        end = time.process_time()
        logger.info(
            f'Ingested processed payload from device {self.device_eui} to geohash "{h}". '
            f'Took: {end - start}s'
        )
        logger.debug(f'Payload: {self.payload}')

    def _update_area_fields(self, area: GeohashArea) -> None:
        updated_data_map = defaultdict(dict)
        updated_status_map = defaultdict(dict)
        updated_metadata_map = area.metadata or {}

        for metric_key, value in self._get_payload_data().items():
            metric = MetricDetailCacheJob().get(key=metric_key)

            updated_metadata_map[metric_key] = self._get_metadata_for(metric)

            for opt_key, opt_val in settings.MOVING_AVERAGE_OPTIONS.items():
                current_data = area.data.get(opt_key, {}).get(metric_key, {})

                updated_data = self._compute_data_for(value, metric, opt_val, current_data)
                updated_status = self._compute_status_for(updated_data, metric)

                updated_data_map[opt_key][metric_key] = updated_data
                updated_status_map[opt_key][metric_key] = updated_status

        area.metadata = updated_metadata_map
        area.data = updated_data_map
        area.status = updated_status_map

    def _has_geo_coordinates(self) -> bool:
        return self.latitude is not None and self.longitude is not None

    def _get_payload_data(self) -> dict:
        return {
            k: v for k, v in self.payload.get('data', {}).items() if k in settings.ELIGIBLE_METRIC_KEYS
        }

    def _compute_data_for(self, value: float, metric: Metric, opt_val: dict, current_data: dict) -> dict:
        updated_data = MovingAverageService(
            relative_time_range=opt_val.get('range'),
            window_size=opt_val.get('window'),
            precision=self.VALUE_PRECISION
        ).update(value, self.payload.get('timestamp'), current_data)

        return updated_data

    def _compute_status_for(self, data: dict, metric: Metric) -> dict:
        try:
            value = data.get('wins', [])[-1].get('y')
        except IndexError as e:
            value = None

        thresholds = metric.metadata.get('thresholds', {})

        # TODO: WTF, why is metric metadata thresholds not updated?
        return StatusService(thresholds).update(value)

    def _update_area_summary(self, area: GeohashArea) -> None:
        updated_summary_map = defaultdict(dict)

        for opt_key, opt_val in settings.MOVING_AVERAGE_OPTIONS.items():
            for category_id, metric_keys in settings.CATEGORY_METRIC_KEYS_MAP.items():
                data_service_class = AGGREGATION_SERVICE_CLASS_MAP.get(category_id)(area)
                updated_summary_map[opt_key][category_id] = data_service_class.compute(opt_key)

        area.summary = updated_summary_map

    def _get_metadata_for(self, metric: Metric) -> dict:
        metadata = metric.metadata or {}

        # Remove useless fields we won't need at area instance level.
        del metadata['thresholds']
        del metadata['description']

        return metadata
