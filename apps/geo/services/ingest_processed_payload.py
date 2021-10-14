import logging
import time

import geohash

from apps.geo.models import GeohashArea

logger = logging.getLogger(__name__)


class IngestProcessedPayloadService(object):
    def __init__(self, device_eui: str, device_type: str, position: dict, payload: dict, **kwargs) -> None:
        self.device_eui = device_eui
        self.device_type = device_type
        self.latitude = position.get('lat')
        self.longitude = position.get('lon')
        self.payload = payload
        self.kwargs = kwargs

    def ingest(self):
        start = time.process_time()

        if not self._has_geo_coordinates():
            logger.debug(f'Missing geo coordinates for device {self.device_eui}. ')
            return

        h = geohash.encode(self.latitude, self.longitude)
        area = GeohashArea.objects.get_or_create(geohash=h)

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
