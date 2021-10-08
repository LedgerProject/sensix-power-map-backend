"""
Project URL config.
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from common.schemas import main_swagger_schema_view

urlpatterns = [
    url(r'^rq/', include('django_rq.urls')),

    url(r'^api/v1/auth/', include('rest_auth.urls')),
    url(r'^api/v1/auth/jwt/login/', TokenObtainPairView.as_view(), name='jwt_token_obtain_pair'),
    url(r'^api/v1/auth/jwt/refresh/', TokenRefreshView.as_view(), name='jwt_token_refresh'),
    url(r'^api/v1/auth/jwt/verify/', TokenVerifyView.as_view(), name='jwt_token_verify'),

    url(r'^api/v1/', include('apps.core.urls')),
    url(r'^api/v1/', include('apps.devices.urls')),

    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^docs/', view=main_swagger_schema_view),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/defender/', include('defender.urls')),

    url(r'^select2/', include('django_select2.urls')),

    url(r'^django-rq/', include('django_rq.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
