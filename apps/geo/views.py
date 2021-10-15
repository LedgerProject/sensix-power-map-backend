from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.geo import serializers
from apps.geo.fields import GeohashAreaFields
from apps.geo.models import GeohashArea


class GeohashAreaViewSet(GeohashAreaFields, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    GeohashArea view set.
    """
    serializer_class = serializers.GeohashAreaSerializer
    queryset = GeohashArea.objects.all()
