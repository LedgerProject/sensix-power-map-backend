from apps.geo.models import Metric, GeohashArea
from common.cache import BaseQuerySetCacheJob


class MetricDetailCacheJob(BaseQuerySetCacheJob):
    model = Metric

    lifetime = 3600
    fetch_on_stale_threshold = 3600

    def fetch(self, *args, **kwargs):
        return super().fetch(*args, **kwargs).first()


class GeohashAreaListCacheJob(BaseQuerySetCacheJob):
    model = GeohashArea

    lifetime = 15
    fetch_on_stale_threshold = 15
