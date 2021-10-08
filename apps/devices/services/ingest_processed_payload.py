import logging
import time

logger = logging.getLogger(__name__)


class IngestProcessedPayloadService(object):
    def __init__(self, device_eui: str, device_type: str, position: dict, payload: dict, **kwargs) -> None:
        self.device_eui = device_eui
        self.device_type = device_type
        self.position = position
        self.payload = payload
        self.kwargs = kwargs

    def ingest(self):
        start = time.process_time()

        # TODO

        end = time.process_time()
        logger.info(
            f'Ingested processed payload from device {self.device_eui}. '
            f'Took: {end - start}s'
        )
        logger.debug(f'Payload: {self.payload}')
