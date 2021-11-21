"""
Common cache.
"""
from cacheback.base import Job
from cacheback.jobs import QuerySetJob
from django.conf import settings


class BaseCacheJob(Job):
    lifetime = settings.DEFAULT_CACHE_DURATION_SECONDS
    fetch_on_stale_threshold = settings.DEFAULT_CACHE_DURATION_SECONDS
    fetch_on_miss = True
    cache_alias = 'default'
    task_options = {'name': settings.RQ_QUEUE_MAP.get('default')}

    def fetch(self, *args, **kwargs):
        raise NotImplementedError


class BaseQuerySetCacheJob(QuerySetJob):
    model = None

    prefetch_related = ()
    select_related = ()

    lifetime = settings.DEFAULT_CACHE_DURATION_SECONDS
    fetch_on_stale_threshold = settings.DEFAULT_CACHE_DURATION_SECONDS
    fetch_on_miss = True
    cache_alias = 'default'
    task_options = {'name': settings.RQ_QUEUE_MAP.get('default')}

    def __init__(self, *args, **kwargs):
        super().__init__(self.model, self.lifetime, self.fetch_on_miss, self.cache_alias, self.task_options)

    def fetch(self, *args, **kwargs):
        qs = self.model.objects.prefetch_related(*self.prefetch_related).select_related(*self.select_related)
        return qs.filter(*args, **kwargs)
