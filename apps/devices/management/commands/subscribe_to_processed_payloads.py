import json
import logging

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.devices import tasks
from common.mqtt import mqtt_service_instance

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Subscribe to MQTT topic to receive device processed payloads, to ingest it'

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

        kwargs = {
            'customerToken': '+',
            'deviceEui': '+'
        }
        topic = settings.MQTT.get('topics', {}).get('device_data')

        assert topic is not None, 'Missing device data MQTT topic'

        client.subscribe(topic)

    @staticmethod
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload)

        device_eui = data['eui']
        device_type = data['type']
        position = data['position']
        payload = data['payload']

        tasks.ingest_processed_payload.delay(device_eui, device_type, position, payload)
