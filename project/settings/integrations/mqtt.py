"""
MQTT Settings.
"""

from project.settings.config import cfg

MQTT = cfg.get('MQTT', {
    'client_id': 'sensix-map-backend',
    'hostname': '127.0.0.1',
    'username': 'sensix',
    'port': 1883,
    'password': 'xxx',
    'topics': {
        'device_data': 'v1/{customerToken}/devices/{deviceEui}/data'
    }
})
