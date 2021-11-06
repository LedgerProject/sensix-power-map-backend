import os
from itertools import chain

from apps.geo import choices
from project.settings.config import cfg

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = os.path.dirname(PROJECT_ROOT)

DEVICE_METRICS_FILE_PATH = cfg.get('DEVICE_METRICS_FILE_PATH', os.path.join(BASE_DIR, 'device_metrics_conf.json'))

MOVING_AVERAGE_DEFAULT_KEY = 'r3'
MOVING_AVERAGE_OPTIONS = {
    'r3': {
        'range': 3 * 60 * 60,  # 3 hours
        'window': 600,  # 10 min
    },
    'r8': {
        'range': 8 * 60 * 60,  # 8 hours
        'window': 1600,  # ~27 min
    },
    'r24': {
        'range': 24 * 60 * 60,  # 24 hours
        'window': 4800,  # 80 min
    },
    'r48': {
        'range': 48 * 60 * 60,  # 48 hours
        'window': 9600,  # 160 min
    }
}

VALUE_PRECISION = 2

THD_AGG_VOLTAGE_METRIC_KEY = 'THV'
THD_AGG_CURRENT_METRIC_KEY = 'THI'

THD_VOLTAGE_METRIC_KEYS = ['THV1', 'THV2', 'THV3']  # Voltage Total Harmonic Distortions
THD_CURRENT_METRIC_KEYS = ['THI1', 'THI2', 'THI3']  # Current Total Harmonic Distortions

THD_METRIC_KEYS = THD_VOLTAGE_METRIC_KEYS + THD_CURRENT_METRIC_KEYS

CATEGORY_METRIC_KEYS_MAP = {
    choices.CATEGORY_POWER_QUALITY_ID: THD_METRIC_KEYS + [
        # L1 Odd Voltage harmonic distortions
        '1V3', '1V5', '1V7', '1V9', '1V11', '1V13', '1V15', '1V17', '1V19', '1V21', '1V23', '1V25', '1V27', '1V29',
        '1V31', '1V33', '1V35', '1V37', '1V39',
        # L2 Odd Voltage harmonic distortions
        '2V3', '2V5', '2V7', '2V9', '2V11', '2V13', '2V15', '2V17', '2V19', '2V21', '2V23', '2V25', '2V27', '2V29',
        '2V31', '2V33', '2V35', '2V37', '2V39',
        # L3 Odd Voltage harmonic distortions
        '3V3', '3V5', '3V7', '3V9', '3V11', '3V13', '3V15', '3V17', '3V19', '3V21', '3V23', '3V25', '3V27', '3V29',
        '3V31', '3V33', '3V35', '3V37', '3V39',
        # L1 Odd Current harmonic distortions
        '1I3', '1I5', '1I7', '1I9', '1I11', '1I13', '1I15', '1I17', '1I19', '1I21', '1I23', '1I25', '1I27', '1I29',
        '1I31', '1I33', '1I35', '1I37', '1I39',
        # L2 Odd Current harmonic distortions
        '2I3', '2I5', '2I7', '2I9', '2I11', '2I13', '2I15', '2I17', '2I19', '2I21', '2I23', '2I25', '2I27', '2I29',
        '2I31', '2I33', '2I35', '2I37', '2I39',
        # L3 Odd Current harmonic distortions
        '3I3', '3I5', '3I7', '3I9', '3I11', '3I13', '3I15', '3I17', '3I19', '3I21', '3I23', '3I25', '3I27', '3I29',
        '3I31', '3I33', '3I35', '3I37', '3I39',
    ],
    choices.CATEGORY_POWER_USAGE_ID: [
        'Pc',  # Cumulated Total Active Power
        'SPc',  # Cumulated Apparent Power
        'fSPc'  # Cumulated Reactive Power
    ]
}

CATEGORY_METRIC_METADATA_MAP = {
    choices.CATEGORY_POWER_QUALITY_ID: {
        THD_AGG_VOLTAGE_METRIC_KEY: {
            'name': 'Voltage THD',
            'text': 'Average Voltage Total Harmonic Distortions',
            'units': '%'
        },
        THD_AGG_CURRENT_METRIC_KEY: {
            'name': 'Current THD',
            'text': 'Average Current Total Harmonic Distortions',
            'units': '%'
        },
        'HDsV': {
            'name': 'Voltage HD',
            'text': 'Voltage Harmonic Distortion',
            'units': '%'
        },
        'HDsI': {
            'name': 'Current HD',
            'text': 'Current Harmonic Distortion',
            'units': '%'
        }
    },
    choices.CATEGORY_POWER_USAGE_ID: {
        'Pc': {
            'name': 'Active Power',
            'text': 'Cumulated Total Active Power',
            'units': 'W'
        },
        'SPc': {
            'name': 'Apparent Power',
            'text': 'Cumulated Apparent Power',
            'units': 'VA'
        },
        'fSPc': {
            'name': 'Reactive Power',
            'text': 'Cumulated Reactive Power',
            'units': 'VAR'
        }
    }
}

ELIGIBLE_METRIC_KEYS = list(chain.from_iterable([metric_keys for metric_keys in CATEGORY_METRIC_KEYS_MAP.values()]))
ELIGIBLE_DEVICE_TYPES = cfg.get('ELIGIBLE_DEVICE_TYPES', ['1P-PowerMonitor1', '3PN-PowerMonitor1'])
