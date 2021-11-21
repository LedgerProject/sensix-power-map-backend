import json

from django.conf import settings

from apps.geo.cache import MetricDetailCacheJob
from apps.geo.models import Metric


class MetricsService(object):

    def __init__(self, file_path: str = None) -> None:
        self.file_path = file_path or settings.DEVICE_METRICS_FILE_PATH

    def load(self):
        with open(self.file_path, 'r') as f:
            Metric.objects.all().delete()

            metrics = json.load(f)

            for metric_key, metadata in metrics.items():
                Metric.objects.create(key=metric_key, metadata=metadata)
                MetricDetailCacheJob().refresh(key=metric_key)
