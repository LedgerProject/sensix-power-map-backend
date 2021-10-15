import logging
import time

import geohash

from apps.geo.models import GeohashArea

logger = logging.getLogger(__name__)


class IngestProcessedPayloadService(object):
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

        h = geohash.encode(self.latitude, self.longitude)
        area, _ = GeohashArea.objects.get_or_create(geohash=h)

        area.status = {'todo': h}
        area.data = {'todo': h}

        area.save(update_fields=['status', 'data'])

        end = time.process_time()
        logger.info(
            f'Ingested processed payload from device {self.device_eui}. '
            f'Took: {end - start}s'
        )
        logger.debug(f'Payload: {self.payload}')

    def _has_geo_coordinates(self):
        return self.latitude is not None and self.longitude is not None
