import mock
from django.test import TestCase

from apps.geo import choices
from apps.geo.services.data import PowerQualityDataService


class PowerQualityDataServiceTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

    def test__compute_single_phase_systems(self):
        status_mock = {
            'time_key': {
                'THV1': {
                    'sid': choices.STATUS_WARNING_ID,
                    'l': 'THD V Some text'
                },
                'THI1': {
                    'sid': choices.STATUS_NORMAL_ID,
                    'l': 'THD I Some text'
                },
                '1V7': {
                    'sid': choices.STATUS_WARNING_ID,
                    'l': 'HD7 I Some text'
                },
            }
        }
        data_mock = {
            'time_key': {
                'THV1': {
                    'agg': {'avg': 2.16},
                    'wins': [
                        {'x': 123, 'y': 5.12, 'cnt': 11, 'max': 11.2, 'min': 0.9},
                        {'x': 123, 'y': 4.54, 'cnt': 11, 'max': 11.2, 'min': 0.9}
                    ]
                },
                'THI1': {
                    'agg': {'avg': 8.66},
                    'wins': [
                        {'x': 123, 'y': 5.42, 'cnt': 11, 'max': 11.2, 'min': 0.9},
                        {'x': 123, 'y': 12.12, 'cnt': 11, 'max': 11.2, 'min': 0.9}
                    ]
                },
                '1V3': {'agg': {'avg': 11.03}},
                '1V5': {'agg': {'avg': 11.05}},
                '1V7': {'agg': {'avg': 11.07}},
                '1V9': {'agg': {'avg': 11.09}},
                '1V11': {'agg': {'avg': 11.11}},
                '1V13': {'agg': {'avg': 11.13}},
                '1V15': {'agg': {'avg': 11.15}},
                '1V17': {'agg': {'avg': 11.17}},
                '1V19': {'agg': {'avg': 11.19}},
                '1V21': {'agg': {'avg': 11.21}},
                '1V23': {'agg': {'avg': 11.23}},
                '1V25': {'agg': {'avg': 11.25}},
                '1V27': {'agg': {'avg': 11.27}},
                '1V29': {'agg': {'avg': 11.29}},
                '1V31': {'agg': {'avg': 11.31}},
                '1V33': {'agg': {'avg': 11.33}},
                '1V35': {'agg': {'avg': 11.35}},
                '1V37': {'agg': {'avg': 11.37}},
                '1V39': {'agg': {'avg': 11.39}},
                '1I3': {'agg': {'avg': 21.03}},
                '1I5': {'agg': {'avg': 21.05}},
                '1I7': {'agg': {'avg': 21.07}},
                '1I9': {'agg': {'avg': 21.09}},
                '1I11': {'agg': {'avg': 21.11}},
                '1I13': {'agg': {'avg': 21.13}},
                '1I15': {'agg': {'avg': 21.15}},
                '1I17': {'agg': {'avg': 21.17}},
                '1I19': {'agg': {'avg': 21.19}},
                '1I21': {'agg': {'avg': 21.21}},
                '1I23': {'agg': {'avg': 21.23}},
                '1I25': {'agg': {'avg': 21.25}},
                '1I27': {'agg': {'avg': 21.27}},
                '1I29': {'agg': {'avg': 21.29}},
                '1I31': {'agg': {'avg': 21.31}},
                '1I33': {'agg': {'avg': 21.33}},
                '1I35': {'agg': {'avg': 21.35}},
                '1I37': {'agg': {'avg': 21.37}},
                '1I39': {'agg': {'avg': 21.39}},
                'will_ignore': {'agg': {'avg': 66.66}},
            }
        }
        area_mock = mock.Mock(data=data_mock, status=status_mock)
        instance = PowerQualityDataService(area_mock)

        actual_result = instance.compute('time_key')

        self.assertEqual(actual_result, {
            'sid': choices.STATUS_WARNING_ID,
            'HDs': [
                {'x': 3, 'y1': 11.03, 'y2': 21.03},
                {'x': 5, 'y1': 11.05, 'y2': 21.05},
                {'x': 7, 'y1': 11.07, 'y2': 21.07},
                {'x': 9, 'y1': 11.09, 'y2': 21.09},
                {'x': 11, 'y1': 11.11, 'y2': 21.11},
                {'x': 13, 'y1': 11.13, 'y2': 21.13},
                {'x': 15, 'y1': 11.15, 'y2': 21.15},
                {'x': 17, 'y1': 11.17, 'y2': 21.17},
                {'x': 19, 'y1': 11.19, 'y2': 21.19},
                {'x': 21, 'y1': 11.21, 'y2': 21.21},
                {'x': 23, 'y1': 11.23, 'y2': 21.23},
                {'x': 25, 'y1': 11.25, 'y2': 21.25},
                {'x': 27, 'y1': 11.27, 'y2': 21.27},
                {'x': 29, 'y1': 11.29, 'y2': 21.29},
                {'x': 31, 'y1': 11.31, 'y2': 21.31},
                {'x': 33, 'y1': 11.33, 'y2': 21.33},
                {'x': 35, 'y1': 11.35, 'y2': 21.35},
                {'x': 37, 'y1': 11.37, 'y2': 21.37},
                {'x': 39, 'y1': 11.39, 'y2': 21.39},
            ],
            'metrics': {
                'THI': {'sid': choices.STATUS_NORMAL_ID,
                        'value': 8.66,
                        'values': [
                            {'x': 123, 'y': 5.42, 'cnt': 11, 'max': 11.2, 'min': 0.9},
                            {'x': 123, 'y': 12.12, 'cnt': 11, 'max': 11.2, 'min': 0.9}
                        ]},
                'THV': {'sid': choices.STATUS_WARNING_ID,
                        'value': 2.16,
                        'values': [
                            {'x': 123, 'y': 5.12, 'cnt': 11, 'max': 11.2, 'min': 0.9},
                            {'x': 123, 'y': 4.54, 'cnt': 11, 'max': 11.2, 'min': 0.9}
                        ]}
            },
            'order': ['THV', 'THI']
        })

    def test__compute_three_phase_systems(self):
        status_mock = {
            'time_key': {
                'THV1': {
                    'sid': choices.STATUS_WARNING_ID,
                    'l': 'THD V1 Some text'
                },
                'THI1': {
                    'sid': choices.STATUS_NORMAL_ID,
                    'l': 'THD I1 Some text'
                },
                'THV3': {
                    'sid': choices.STATUS_NORMAL_ID,
                    'l': 'THD V3 Some text'
                },
                'THI3': {
                    'sid': choices.STATUS_CRITICAL_ID,
                    'l': 'THD I3 Some text'
                },
                '1V7': {
                    'sid': choices.STATUS_WARNING_ID,
                    'l': 'HD7 I Some text'
                },
            }
        }
        data_mock = {
            'time_key': {
                'THV1': {
                    'agg': {'avg': 11.26},
                    'wins': [
                        {'x': 101, 'y': 11.11, 'cnt': 11, 'max': 19.11, 'min': 10.01},
                        {'x': 201, 'y': 11.21, 'cnt': 12, 'max': 19.21, 'min': 10.21},
                        {'x': 301, 'y': 11.31, 'cnt': 13, 'max': 19.31, 'min': 10.31},
                        {'x': 401, 'y': 11.41, 'cnt': 14, 'max': 19.41, 'min': 10.41},
                    ]
                },
                'THI1': {
                    'agg': {'avg': 1.26},
                    'wins': [
                        {'x': 101, 'y': 1.11, 'cnt': 11, 'max': 9.11, 'min': 0.01},
                        {'x': 201, 'y': 1.21, 'cnt': 12, 'max': 9.21, 'min': 0.21},
                        {'x': 301, 'y': 1.31, 'cnt': 13, 'max': 9.31, 'min': 0.31},
                        {'x': 401, 'y': 1.41, 'cnt': 14, 'max': 9.41, 'min': 0.41},
                    ]
                },
                'THV2': {
                    'agg': {'avg': 21.26},
                    'wins': [
                        {'x': 101, 'y': 21.11, 'cnt': 11, 'max': 29.11, 'min': 20.01},
                        {'x': 201, 'y': 21.21, 'cnt': 12, 'max': 29.21, 'min': 20.21},
                        {'x': 301, 'y': 21.31, 'cnt': 13, 'max': 29.31, 'min': 20.31},
                        {'x': 401, 'y': 21.41, 'cnt': 14, 'max': 29.41, 'min': 20.41},
                    ]
                },
                'THI2': {
                    'agg': {'avg': 121.26},
                    'wins': [
                        {'x': 101, 'y': 121.11, 'cnt': 11, 'max': 129.11, 'min': 120.01},
                        {'x': 201, 'y': 121.21, 'cnt': 12, 'max': 129.21, 'min': 120.21},
                        {'x': 301, 'y': 121.31, 'cnt': 13, 'max': 129.31, 'min': 120.31},
                        {'x': 401, 'y': 121.41, 'cnt': 14, 'max': 129.41, 'min': 120.41},
                    ]
                },
                'THV3': {
                    'agg': {'avg': 131.26},
                    'wins': [
                        {'x': 101, 'y': 131.11, 'cnt': 11, 'max': 139.11, 'min': 130.01},
                        {'x': 201, 'y': 131.21, 'cnt': 12, 'max': 139.21, 'min': 130.21},
                        {'x': 301, 'y': 131.31, 'cnt': 13, 'max': 139.31, 'min': 130.31},
                        {'x': 401, 'y': 131.41, 'cnt': 14, 'max': 139.41, 'min': 130.41},
                    ]
                },
                'THI3': {
                    'agg': {'avg': 31.26},
                    'wins': [
                        {'x': 101, 'y': 31.11, 'cnt': 11, 'max': 39.11, 'min': 30.01},
                        {'x': 201, 'y': 31.21, 'cnt': 12, 'max': 39.21, 'min': 30.21},
                        {'x': 301, 'y': 31.31, 'cnt': 13, 'max': 39.31, 'min': 30.31},
                        {'x': 401, 'y': 31.41, 'cnt': 14, 'max': 39.41, 'min': 30.41},
                    ]
                },
                '1V3': {'agg': {'avg': 11.03}}, '2V3': {'agg': {'avg': 111.03}}, '3V3': {'agg': {'avg': 311.03}},
                '1V5': {'agg': {'avg': 11.05}}, '2V5': {'agg': {'avg': 111.05}}, '3V5': {'agg': {'avg': 311.05}},
                '1V7': {'agg': {'avg': 11.07}}, '2V7': {'agg': {'avg': 111.07}}, '3V7': {'agg': {'avg': 311.07}},
                '1V9': {'agg': {'avg': 11.09}}, '2V9': {'agg': {'avg': 111.09}}, '3V9': {'agg': {'avg': 311.09}},
                '1V11': {'agg': {'avg': 11.11}}, '2V11': {'agg': {'avg': 111.11}}, '3V11': {'agg': {'avg': 311.11}},
                '1V13': {'agg': {'avg': 11.13}}, '2V13': {'agg': {'avg': 111.13}}, '3V13': {'agg': {'avg': 311.13}},
                '1V15': {'agg': {'avg': 11.15}}, '2V15': {'agg': {'avg': 111.15}}, '3V15': {'agg': {'avg': 311.15}},
                '1V17': {'agg': {'avg': 11.17}}, '2V17': {'agg': {'avg': 111.17}}, '3V17': {'agg': {'avg': 311.17}},
                '1V19': {'agg': {'avg': 11.19}}, '2V19': {'agg': {'avg': 111.19}}, '3V19': {'agg': {'avg': 311.19}},
                '1V21': {'agg': {'avg': 11.21}}, '2V21': {'agg': {'avg': 111.21}}, '3V21': {'agg': {'avg': 311.21}},
                '1V23': {'agg': {'avg': 11.23}}, '2V23': {'agg': {'avg': 111.23}}, '3V23': {'agg': {'avg': 311.23}},
                '1V25': {'agg': {'avg': 11.25}}, '2V25': {'agg': {'avg': 111.25}}, '3V25': {'agg': {'avg': 311.25}},
                '1V27': {'agg': {'avg': 11.27}}, '2V27': {'agg': {'avg': 111.27}}, '3V27': {'agg': {'avg': 311.27}},
                '1V29': {'agg': {'avg': 11.29}}, '2V29': {'agg': {'avg': 111.29}}, '3V29': {'agg': {'avg': 311.29}},
                '1V31': {'agg': {'avg': 11.31}}, '2V31': {'agg': {'avg': 111.31}}, '3V31': {'agg': {'avg': 311.31}},
                '1V33': {'agg': {'avg': 11.33}}, '2V33': {'agg': {'avg': 111.33}}, '3V33': {'agg': {'avg': 311.33}},
                '1V35': {'agg': {'avg': 11.35}}, '2V35': {'agg': {'avg': 111.35}}, '3V35': {'agg': {'avg': 311.35}},
                '1V37': {'agg': {'avg': 11.37}}, '2V37': {'agg': {'avg': 111.37}}, '3V37': {'agg': {'avg': 311.37}},
                '1V39': {'agg': {'avg': 11.39}}, '2V39': {'agg': {'avg': 111.39}}, '3V39': {'agg': {'avg': 311.39}},
                '1I3': {'agg': {'avg': 21.03}}, '2I3': {'agg': {'avg': 121.03}}, '3I3': {'agg': {'avg': 321.03}},
                '1I5': {'agg': {'avg': 21.05}}, '2I5': {'agg': {'avg': 121.05}}, '3I5': {'agg': {'avg': 321.05}},
                '1I7': {'agg': {'avg': 21.07}}, '2I7': {'agg': {'avg': 121.07}}, '3I7': {'agg': {'avg': 321.07}},
                '1I9': {'agg': {'avg': 21.09}}, '2I9': {'agg': {'avg': 121.09}}, '3I9': {'agg': {'avg': 321.09}},
                '1I11': {'agg': {'avg': 21.11}}, '2I11': {'agg': {'avg': 121.11}}, '3I11': {'agg': {'avg': 321.11}},
                '1I13': {'agg': {'avg': 21.13}}, '2I13': {'agg': {'avg': 121.13}}, '3I13': {'agg': {'avg': 321.13}},
                '1I15': {'agg': {'avg': 21.15}}, '2I15': {'agg': {'avg': 121.15}}, '3I15': {'agg': {'avg': 321.15}},
                '1I17': {'agg': {'avg': 21.17}}, '2I17': {'agg': {'avg': 121.17}}, '3I17': {'agg': {'avg': 321.17}},
                '1I19': {'agg': {'avg': 21.19}}, '2I19': {'agg': {'avg': 121.19}}, '3I19': {'agg': {'avg': 321.19}},
                '1I21': {'agg': {'avg': 21.21}}, '2I21': {'agg': {'avg': 121.21}}, '3I21': {'agg': {'avg': 321.21}},
                '1I23': {'agg': {'avg': 21.23}}, '2I23': {'agg': {'avg': 121.23}}, '3I23': {'agg': {'avg': 321.23}},
                '1I25': {'agg': {'avg': 21.25}}, '2I25': {'agg': {'avg': 121.25}}, '3I25': {'agg': {'avg': 321.25}},
                '1I27': {'agg': {'avg': 21.27}}, '2I27': {'agg': {'avg': 121.27}}, '3I27': {'agg': {'avg': 321.27}},
                '1I29': {'agg': {'avg': 21.29}}, '2I29': {'agg': {'avg': 121.29}}, '3I29': {'agg': {'avg': 321.29}},
                '1I31': {'agg': {'avg': 21.31}}, '2I31': {'agg': {'avg': 121.31}}, '3I31': {'agg': {'avg': 321.31}},
                '1I33': {'agg': {'avg': 21.33}}, '2I33': {'agg': {'avg': 121.33}}, '3I33': {'agg': {'avg': 321.33}},
                '1I35': {'agg': {'avg': 21.35}}, '2I35': {'agg': {'avg': 121.35}}, '3I35': {'agg': {'avg': 321.35}},
                '1I37': {'agg': {'avg': 21.37}}, '2I37': {'agg': {'avg': 121.37}}, '3I37': {'agg': {'avg': 321.37}},
                '1I39': {'agg': {'avg': 21.39}}, '2I39': {'agg': {'avg': 121.39}}, '3I39': {'agg': {'avg': 321.39}},
                'will_ignore': {'agg': {'avg': 66.66}},
            }
        }
        area_mock = mock.Mock(data=data_mock, status=status_mock)
        instance = PowerQualityDataService(area_mock)

        actual_result = instance.compute('time_key')

        self.assertEqual(actual_result, {
            'sid': choices.STATUS_CRITICAL_ID,
            'HDs': [
                {'x': 3, 'y1': 144.36, 'y2': 154.36},
                {'x': 5, 'y1': 144.38, 'y2': 154.38},
                {'x': 7, 'y1': 144.4, 'y2': 154.4},
                {'x': 9, 'y1': 144.42, 'y2': 154.42},
                {'x': 11, 'y1': 144.44, 'y2': 154.44},
                {'x': 13, 'y1': 144.46, 'y2': 154.46},
                {'x': 15, 'y1': 144.48, 'y2': 154.48},
                {'x': 17, 'y1': 144.5, 'y2': 154.5},
                {'x': 19, 'y1': 144.52, 'y2': 154.52},
                {'x': 21, 'y1': 144.54, 'y2': 154.54},
                {'x': 23, 'y1': 144.56, 'y2': 154.56},
                {'x': 25, 'y1': 144.58, 'y2': 154.58},
                {'x': 27, 'y1': 144.6, 'y2': 154.6},
                {'x': 29, 'y1': 144.62, 'y2': 154.62},
                {'x': 31, 'y1': 144.64, 'y2': 154.64},
                {'x': 33, 'y1': 144.66, 'y2': 154.66},
                {'x': 35, 'y1': 144.68, 'y2': 154.68},
                {'x': 37, 'y1': 144.7, 'y2': 154.7},
                {'x': 39, 'y1': 144.72, 'y2': 154.72}
            ],
            'metrics': {
                'THI': {'sid': choices.STATUS_CRITICAL_ID,
                        'value': 51.26,
                        'values': [
                            {'x': 101, 'y': 51.11, 'cnt': 11, 'max': 129.11, 'min': 0.01},
                            {'x': 201, 'y': 51.21, 'cnt': 12, 'max': 129.21, 'min': 0.21},
                            {'x': 301, 'y': 51.31, 'cnt': 13, 'max': 129.31, 'min': 0.31},
                            {'x': 401, 'y': 51.41, 'cnt': 14, 'max': 129.41, 'min': 0.41}
                        ]},
                'THV': {'sid': choices.STATUS_WARNING_ID,
                        'value': 54.59,
                        'values': [
                            {'x': 101, 'y': 54.44, 'cnt': 11, 'max': 139.11, 'min': 10.01},
                            {'x': 201, 'y': 54.54, 'cnt': 12, 'max': 139.21, 'min': 10.21},
                            {'x': 301, 'y': 54.64, 'cnt': 13, 'max': 139.31, 'min': 10.31},
                            {'x': 401, 'y': 54.74, 'cnt': 14, 'max': 139.41, 'min': 10.41}
                        ]}
            },
            'order': ['THV', 'THI']
        })

    def test__get_agg_values_for(self):
        data_mock = {
            'time_key': {
                'key1': {
                    'wins': [
                        {'x': 101, 'y': 12.11, 'cnt': 12, 'max': 12.11, 'min': 11.11},
                        {'x': 201, 'y': 12.22, 'cnt': 10, 'max': 12.22, 'min': 11.22},
                        {'x': 301, 'y': 12.33, 'cnt': 9, 'max': 12.33, 'min': 11.33},
                        {'x': 401, 'y': 12.44, 'cnt': 6, 'max': 12.44, 'min': 11.44},
                        {'x': 501, 'y': 12.55, 'cnt': 3, 'max': 12.55, 'min': 11.55},
                    ]
                },
                'key2': {
                    'wins': [
                        {'x': 302, 'y': 22.33, 'cnt': 11, 'max': 22.33, 'min': 21.33},
                        {'x': 402, 'y': 22.44, 'cnt': 1, 'max': 22.44, 'min': 21.44},
                        {'x': 502, 'y': 22.55, 'cnt': 4, 'max': 22.55, 'min': 21.55},
                    ]
                },
                'key3': {
                    'wins': [
                        {'x': 503, 'y': 32.55, 'cnt': 12, 'max': 32.55, 'min': 31.55},
                    ]
                },
                'key4': {}
            }
        }

        area_mock = mock.Mock(data=data_mock)
        instance = PowerQualityDataService(area_mock)

        actual_result = instance._get_agg_values_for('time_key', ['key3', 'key2', 'key1', 'key4'])

        self.assertEqual(actual_result, [
            {'x': 101, 'y': 12.11, 'cnt': 12, 'max': 12.11, 'min': 11.11},
            {'x': 201, 'y': 12.22, 'cnt': 10, 'max': 12.22, 'min': 11.22},
            {'x': 302, 'y': 17.33, 'cnt': 11, 'max': 22.33, 'min': 11.33},
            {'x': 402, 'y': 17.44, 'cnt': 6, 'max': 22.44, 'min': 11.44},
            {'x': 503, 'y': 22.55, 'cnt': 12, 'max': 32.55, 'min': 11.55},
        ])
