from rest_framework import routers

from apps.geo.views import GeohashAreaViewSet

router = routers.SimpleRouter()

router.register('geohash-area', GeohashAreaViewSet, basename='geohash-area')

urlpatterns = [
]

urlpatterns += router.urls
