"""
Devices RQ tasks.
"""

import logging

from django.conf import settings
from django_rq import job

from apps.devices.services.ingest_processed_payload import IngestProcessedPayloadService

logger = logging.getLogger(__name__)


@job(settings.RQ_QUEUE_MAP.get('ingest'), timeout='10s')
def ingest_processed_payload(device_eui: str, device_type: str, position: dict, payload: dict, **kwargs):
    IngestProcessedPayloadService(device_eui, device_type, position, payload, **kwargs).ingest()
