"""
Creates a default superuser.
"""
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates a default superuser'

    def handle(self, *args, **options):
        username = settings.ADMIN_USERNAME
        password = settings.ADMIN_PASSWORD

        try:
            User.objects.create_user(username, 'say@sensidev.com', password, is_superuser=True, is_staff=True)
        except IntegrityError:
            logger.info('The superuser `{}` already exists'.format(username))
            self._update_passowrd(username, password)

    def _update_passowrd(self, username, password):
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        logger.info('Password updated')
