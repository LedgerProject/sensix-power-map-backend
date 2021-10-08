"""
Django admin login defender configs.
https://github.com/kencochrane/django-defender
"""

from project.settings.config import cfg

DEFENDER_LOGIN_FAILURE_LIMIT = 5
DEFENDER_REDIS_URL = cfg.get('CACHES', {}).get('default', {}).get('LOCATION', 'redis://localhost:6379/0')
DEFENDER_COOLOFF_TIME = 600
DEFENDER_ACCESS_ATTEMPT_EXPIRATION = 168
DEFENDER_CACHE_PREFIX = '{}-defender'.format(cfg.get('CACHES', {}).get('default', {}).get('KEY_PREFIX', 'devices'))
