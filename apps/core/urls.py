"""
Core Urls.
"""
from django.urls import path

from apps.core.views import TestSentryAPIView, VersionView

urlpatterns = [

    path('sentry/test/', TestSentryAPIView.as_view(), name='sentry-test-exception'),
    path('version/', VersionView.as_view(), name='version-detail'),
]
