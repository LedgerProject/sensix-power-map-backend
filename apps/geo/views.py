from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.geo import serializers
from apps.geo.fields import GeohashAreaFields
from apps.geo.models import GeohashArea


class GeohashAreaViewSet(GeohashAreaFields, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    GeohashArea view set.
    """
    serializer_class = serializers.GeohashAreaDetailSerializer
    queryset = GeohashArea.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GeohashAreaListSerializer
        else:
            return self.serializer_class
