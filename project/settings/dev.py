"""
Dev Settings.
"""

try:
    from .common import *
except ImportError as e:
    raise e

DEBUG = True

ALLOWED_HOSTS = ['*']

FILER_DEBUG = True
FILER_ENABLE_LOGGING = True

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

CORS_ORIGIN_ALLOW_ALL = True

# Switch to synchronous mode for RQ Worker
try:
    for queueConfig in RQ_QUEUES.values():
        queueConfig['ASYNC'] = False
except (NameError, AttributeError, KeyError):
    pass

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
        'level': 'DEBUG',
        'propagate': False,
    },
    'apps': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'redis_cache': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'rq.worker': {
        'handlers': ['rq_console'],
        'level': 'DEBUG'
    },
    'cacheback': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
    },
    'filer': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'common': {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'requests': {
        'handlers': ['null'],
    },
    'drf_requests_jwt': {
        'handlers': ['console'],
        'level': 'DEBUG'
    },
}
