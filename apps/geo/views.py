from django.conf import settings
from rest_framework import mixins, permissions
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.geo import serializers, choices
from apps.geo.cache import GeohashAreaListCacheJob, GeohashAreaDetailCacheJob
from apps.geo.fields import GeohashAreaFields


class GeohashAreaViewSet(GeohashAreaFields, mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    GeohashArea view set.
    """
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        pass

    def _get_query_param(self, field_name: str, default: str = None) -> str:
        return self.request.query_params.get(field_name, default)

    def list(self, request, *args, **kwargs):
        kwargs = {
            'time_range': self._get_query_param('relative_time_range', settings.MOVING_AVERAGE_DEFAULT_KEY),
            'category_id': self._get_query_param('category_id', choices.CATEGORY_POWER_QUALITY_ID)
        }

        queryset = GeohashAreaListCacheJob().get(**kwargs)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.GeohashAreaListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.GeohashAreaListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        kwargs = {
            'geohash': self.kwargs.get('pk'),
            'time_range': self._get_query_param('relative_time_range', settings.MOVING_AVERAGE_DEFAULT_KEY),
            'category_id': self._get_query_param('category_id', choices.CATEGORY_POWER_QUALITY_ID)
        }

        instance = GeohashAreaDetailCacheJob().get(**kwargs)
        serializer = serializers.GeohashAreaDetailSerializer(instance)
        return Response(serializer.data)
