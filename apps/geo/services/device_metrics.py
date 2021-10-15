import json

from django.conf import settings

class DeviceMetricsService(object):

    def __init__(self, file_path: str = None) -> None:
        self.file_path = file_path or settings.DEVICE_METRICS_FILE_PATH

    def load(self):
        with open(self.file_path, 'r') as f:
            metrics = json.load(f)

        return metrics
