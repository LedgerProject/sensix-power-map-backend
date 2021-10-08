"""
VPS Prod Settings.
"""

try:
    from .common import *
except ImportError as e:
    if cfg.get('SENTRY_IO_ENABLED', False):
        import sentry_sdk

        sentry_sdk.capture_exception(e)
        raise e

DEBUG = False

# HTTPS settings
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 3600

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = False  # It runs as a proxy behind Nginx
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_PRELOAD = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = cfg.get('EMAIL_USE_TLS')
EMAIL_HOST = cfg.get('EMAIL_HOST')
EMAIL_HOST_USER = cfg.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = cfg.get('EMAIL_HOST_PASSWORD')
EMAIL_PORT = cfg.get('EMAIL_PORT')

LOGGING['loggers'] = {
    'django': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'django.request': {
        'handlers': ['console'],
        'level': 'ERROR',
        'propagate': True,
    },
    'django.db.backends': {
        'handlers': ['console'],
        'propagate': False,
    },
    'apps': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
    },
    'redis_cache': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
    },
    'rq.worker': {
        'handlers': ['rq_console'],
        'level': 'INFO'
    },
    'filer': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': True,
    },
    'requests': {
        'handlers': ['null'],
    },
    'drf_requests_jwt': {
        'handlers': ['console'],
        'level': 'INFO'
    },
}
