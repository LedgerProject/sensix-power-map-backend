from django.contrib.postgres.fields import JSONField
from django.db import models


class GeohashArea(models.Model):
    geohash = models.CharField(max_length=16, primary_key=True, help_text='Geohash of the map area')

    status = JSONField(default=dict, blank=True, null=True, help_text='Aggregated status for given geohash')
    data = JSONField(default=dict, blank=True, null=True, help_text='Aggregated data for given geohash')

