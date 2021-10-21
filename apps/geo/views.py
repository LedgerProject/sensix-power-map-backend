from rest_framework import mixins, permissions
from rest_framework.viewsets import GenericViewSet

from apps.geo import serializers
from apps.geo.cache import GeohashAreaListCacheJob
from apps.geo.fields import GeohashAreaFields


class GeohashAreaViewSet(GeohashAreaFields, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    GeohashArea view set.
    """
    permission_classes = permissions.AllowAny
    serializer_class = serializers.GeohashAreaDetailSerializer

    def get_queryset(self):
        return GeohashAreaListCacheJob().get()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.GeohashAreaListSerializer
        else:
            return self.serializer_class
