"""
MQTT service.
"""
import json
import logging

from paho.mqtt.client import Client, MQTTv311

logger = logging.getLogger(__name__)


class MQTTService(object):
    """
    MQTT Service wrapping a paho mqtt client.
    """

    def __init__(self,
                 client_id: str, hostname: str, port: int,
                 username: str = None, password: str = None,
                 async_api_specs: dict = None):
        self.client_id = client_id
        self.hostname = hostname
        self.port = port
        self.async_api_specs = async_api_specs or {}

        self._client = Client(
            client_id=client_id, clean_session=True,
            userdata=None, protocol=MQTTv311, transport='tcp'
        )

        self._client.enable_logger(logger)

        if username:
            self._client.username_pw_set(username=username, password=password)

        self._client.on_connect = self._on_connect_default_callback
        self._client.on_message = self._on_message_default_callback

    @staticmethod
    def _on_connect_default_callback(client, userdata, flags, rc):
        logger.info('Connected with result code {}'.format(rc))

    @staticmethod
    def _on_message_default_callback(client, userdata, msg):
        payload = json.loads(msg.payload)
        logger.info('Received payload {}'.format(payload))

    @property
    def client(self):
        return self._client

    def connect(self):
        self._client.connect(self.hostname, self.port, 60)

    def disconnect(self):
        self._client.disconnect()
