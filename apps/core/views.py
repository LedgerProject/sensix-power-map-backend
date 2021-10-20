"""
Core Views.
"""

import subprocess

from apps.core.serializers import VersionSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class VersionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        git_version = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'])

        serializer = VersionSerializer(data={'version': git_version.decode('utf-8')})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


class TestSentryAPIView(APIView):
    """
    Test sentry.io
    """

    def get(self, request):
        x = 1 / 0
