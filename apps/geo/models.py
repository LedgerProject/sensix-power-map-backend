from django.contrib.postgres.fields import JSONField
from django.db import models


class GeohashArea(models.Model):
    geohash = models.CharField(max_length=16, primary_key=True, help_text='Geohash of the map area')

    summary = JSONField(default=dict, blank=True, null=True, help_text='Aggregated summary for each category')

    metadata = JSONField(default=dict, blank=True, null=True, help_text='Metadata')

    status = JSONField(default=dict, blank=True, null=True, help_text='Aggregated status')
    data = JSONField(default=dict, blank=True, null=True, help_text='Aggregated data for given geohash area')

    def __str__(self):
        return self.geohash


class Metric(models.Model):
    key = models.CharField(max_length=4, primary_key=True, help_text='Metric key identifier')

    metadata = JSONField(default=dict, blank=True, null=True, help_text='Metric metadata')

    def __str__(self):
        return self.key
