"""
MQTT service instance, acting as a singleton.
"""
import uuid

from django.conf import settings

from common.services.mqtt import MQTTService

client_id = settings.MQTT['client_id']
random_hash = uuid.uuid4().hex[:16]

mqtt_service_instance = MQTTService(
    client_id=f'{client_id}-main-{random_hash}',
    hostname=settings.MQTT['hostname'],
    port=settings.MQTT['port'],
    username=settings.MQTT.get('username'),
    password=settings.MQTT.get('password'),
)
