"""
Codeship test settings.
"""
try:
    from project.settings.common import *
except ImportError:
    pass

try:
    from project.settings.tests.common import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': '127.0.0.1',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/test-users-{}'.format(datetime.datetime.now()),
        'KEY_PREFIX': 'test-users'
    }
}
