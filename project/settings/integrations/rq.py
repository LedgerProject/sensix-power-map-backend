"""
Django RQ, managing our RQ queues
https://github.com/rq/django-rq
"""

from project.settings.config import cfg

RQ_SHOW_ADMIN_LINK = True

RQ_QUEUE_MAP = cfg.get('RQ_QUEUE_MAP', {})

RQ_QUEUES = {
    v: {
        'USE_REDIS_CACHE': 'default',
    } for v in RQ_QUEUE_MAP.values()
}
