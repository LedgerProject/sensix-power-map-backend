"""
Common test settings.
"""
try:
    from project.settings.dev import *
except ImportError:
    pass

DEFENDER_REDIS_URL = 'redis://localhost:6666/66'

RQ_QUEUES = {
    'default': {}
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/test-users-{}'.format(datetime.datetime.now()),
        'KEY_PREFIX': 'test-users'
    }
}