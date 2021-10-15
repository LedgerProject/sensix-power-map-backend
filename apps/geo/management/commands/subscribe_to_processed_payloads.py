import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.geo import tasks
from apps.geo.services.device_metrics import DeviceMetricsService
from common.mqtt import mqtt_service_instance

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Subscribe to MQTT topic to receive device processed payloads, to ingest it'
    DEVICE_METRICS_MAP = DeviceMetricsService().load()

    def handle(self, *args, **options):
        mqtt_service_instance.client.enable_logger(logger)

        mqtt_service_instance.client.on_connect = self.on_connect
        mqtt_service_instance.client.on_message = self.on_message

        mqtt_service_instance.connect()

        mqtt_service_instance.client.loop_forever()

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        logger.info('Connected with result code {}'.format(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.

        topic_pattern = settings.MQTT.get('topics', {}).get('device_data')

        assert topic_pattern is not None, 'Missing device data MQTT topic'

        kwargs = {
            'customerToken': '+',
            'deviceEui': '+'
        }
        topic = topic_pattern.format(**kwargs)

        client.subscribe(topic)

    @staticmethod
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload)

        tasks.ingest_processed_payload.delay(data, Command.DEVICE_METRICS_MAP)
