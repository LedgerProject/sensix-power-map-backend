import logging
import time

import geohash

logger = logging.getLogger(__name__)


class IngestProcessedPayloadService(object):
    def __init__(self, device_eui: str, device_type: str, position: dict, payload: dict, **kwargs) -> None:
        self.device_eui = device_eui
        self.device_type = device_type
        self.position_lat = position.get('lat')
        self.position_lon = position.get('lon')
        self.payload = payload
        self.kwargs = kwargs

    def ingest(self):
        start = time.process_time()

        if self._has_geo_coordinates():
            h = geohash.encode(self.position_lat, self.position_lon)



        end = time.process_time()
        logger.info(
            f'Ingested processed payload from device {self.device_eui}. '
            f'Took: {end - start}s'
        )
        logger.debug(f'Payload: {self.payload}')

    def _has_geo_coordinates(self):
        return self.position_lat is not None and self.position_lon is not None
