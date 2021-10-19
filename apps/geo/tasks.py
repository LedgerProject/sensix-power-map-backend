import logging

from django.conf import settings
from django_rq import job

from apps.geo.services.ingest_processed_payload import IngestProcessedPayloadService

logger = logging.getLogger(__name__)


@job(settings.RQ_QUEUE_MAP.get('default'), timeout='10s')
def ingest_processed_payload(data: dict, **kwargs):
    IngestProcessedPayloadService(data, **kwargs).ingest()
