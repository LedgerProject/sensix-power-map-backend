"""
Core Exceptions.
"""
import logging

from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.exceptions import _get_error_details
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def _get_message_for(detail):
    if detail:
        if isinstance(detail, dict):
            first_error = list(detail.items())[0]
            return _get_message_for(first_error[1])
        elif isinstance(detail, list):
            return _get_message_for(detail[0])
        else:
            return force_text(detail).capitalize()
    return None


def _enhanced_APIExcepton__init__(self, detail=None, code=None):
    if detail is None:
        detail = self.default_detail
    if code is None:
        code = self.default_code

    self.message = _get_message_for(detail) or self.default_message

    self.detail = _get_error_details(detail, code)


def _enhanced_ValidationError__init__(self, detail=None, code=None):
    if detail is None:
        detail = self.default_detail
    if code is None:
        code = self.default_code

    self.message = _get_message_for(detail) or self.default_message

    # For validation failures, we may collect many errors together,
    # so the details should always be coerced to a list if not already.
    if not isinstance(detail, dict) and not isinstance(detail, list):
        detail = [detail]

    self.detail = _get_error_details(detail, code)


def message_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if hasattr(exc, 'message'):
        message = exc.message
    else:
        message = force_text(exc)

    if response is None:
        response = Response({}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, headers={})

    if response is not None:
        response.data = {
            'message': message,
            'details': response.data
        }

    logger.info('Received exception: {}', exc)

    if response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.exception(exc)

    return response


# Monkey-patch APIException to support message object
exceptions.APIException.default_message = _('A server error occurred.')
exceptions.APIException.__init__ = _enhanced_APIExcepton__init__
exceptions.ValidationError.__init__ = _enhanced_ValidationError__init__
