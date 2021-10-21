from django.db.models import F, Func, Value, IntegerField, TextField

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

    def fetch(self, *args, **kwargs):
        time_range = kwargs.get('time_range')
        category_id = kwargs.get('category_id')

        qs = GeohashArea.objects.all().annotate(
            h=F('geohash'),
            sid=Func(
                F('agg_status'), Value(time_range), Value(category_id),
                function='jsonb_extract_path_text',
                output_field=IntegerField()
            )
        ).values(
            'sid'
        )

        return qs


class GeohashAreaDetailCacheJob(BaseQuerySetCacheJob):
    model = GeohashArea

    lifetime = 15
    fetch_on_stale_threshold = 15

    def fetch(self, *args, **kwargs):
        geohash = kwargs.get('geohash')
        time_range = kwargs.get('time_range')
        category_id = kwargs.get('category_id')

        qs = GeohashArea.objects.annotate(
            h=F('geohash'),
            sid=Func(
                F('agg_status'), Value(time_range), Value(category_id),
                function='jsonb_extract_path_text',
                output_field=IntegerField()
            ),
            agg_data_subset=Func(
                F('agg_data'), Value(time_range), Value(category_id),
                function='jsonb_extract_path_text',
                output_field=TextField()
            )
        ).get(
            geohash=geohash
        )

        return qs
