"""
Prod test settings.
"""
try:
    from project.settings.prod import *
except ImportError:
    pass

try:
    from project.settings.tests.common import *
except ImportError:
    pass

RQ_QUEUES = {
    'default': {},
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/test-users-{}'.format(datetime.datetime.now()),
        'KEY_PREFIX': 'test-users'
    }
}
