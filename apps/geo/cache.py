from apps.geo.models import Metric
from common.cache import BaseQuerySetCacheJob


class MetricDetailCacheJob(BaseQuerySetCacheJob):
    model = Metric

    lifetime = 3600
    fetch_on_stale_threshold = 3600

    def fetch(self, *args, **kwargs):
        return super().fetch(*args, **kwargs).first()
