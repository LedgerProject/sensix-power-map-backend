from django.contrib.postgres.fields import JSONField
from django.db import models


class GeohashArea(models.Model):
    geohash = models.CharField(max_length=16, primary_key=True, help_text='Geohash of the map area')

    agg_status = JSONField(
        help_text='Aggregated status for each time range and each category',
        default=dict, blank=True, null=True
    )
    agg_data = JSONField(
        help_text='Aggregated data for each time range and each category',
        default=dict, blank=True, null=True
    )
    metadata = JSONField(
        help_text='Metadata for each metric',
        default=dict, blank=True, null=True
    )
    status = JSONField(
        help_text='Status for each time range and each metric',
        default=dict, blank=True, null=True
    )
    data = JSONField(
        help_text='Moving average data for each time_range and each metric',
        default=dict, blank=True, null=True
    )

    def __str__(self):
        return self.geohash


class Metric(models.Model):
    key = models.CharField(max_length=4, primary_key=True, help_text='Metric key identifier')

    metadata = JSONField(default=dict, blank=True, null=True, help_text='Metric metadata')

    def __str__(self):
        return self.key
