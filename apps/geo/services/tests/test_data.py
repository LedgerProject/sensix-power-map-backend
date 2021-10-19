import mock
from django.test import TestCase

from apps.geo import choices
from apps.geo.services.data import PowerQualityDataService


class PowerQualityDataServiceTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

    def test_compute(self):
        status_mock = {
            'time_key': {
                'THV': {
                    'sid': choices.STATUS_WARNING_ID,
                    'l': 'THD V Some text'
                },
                'THI': {
                    'sid': choices.STATUS_NORMAL_ID,
                    'l': 'THD I Some text'
                },
            }
        }
        data_mock = {
            'time_key': {
                'THV': {
                    'agg': {'lv': 2.16},
                    'wins': [{'x': 123, 'y': 5.12}, {'x': 123, 'y': 4.54}]
                },
                'THI': {
                    'agg': {'lv': 8.66},
                    'wins': [{'x': 123, 'y': 5.42}, {'x': 123, 'y': 12.12}]
                },
                '1V3': {'agg': {'lv': 11.03}},
                '1V5': {'agg': {'lv': 11.05}},
                '1V7': {'agg': {'lv': 11.07}},
                '1V9': {'agg': {'lv': 11.09}},
                '1V11': {'agg': {'lv': 11.11}},
                '1V13': {'agg': {'lv': 11.13}},
                '1V15': {'agg': {'lv': 11.15}},
                '1V17': {'agg': {'lv': 11.17}},
                '1V19': {'agg': {'lv': 11.19}},
                '1V21': {'agg': {'lv': 11.21}},
                '1V22': {'agg': {'lv': 11.22}},
                '1V23': {'agg': {'lv': 11.23}},
                '1I3': {'agg': {'lv': 21.03}},
                '1I5': {'agg': {'lv': 21.05}},
                '1I7': {'agg': {'lv': 21.07}},
                '1I9': {'agg': {'lv': 21.09}},
                '1I11': {'agg': {'lv': 21.11}},
                '1I13': {'agg': {'lv': 21.13}},
                '1I15': {'agg': {'lv': 21.15}},
                '1I17': {'agg': {'lv': 21.17}},
                '1I19': {'agg': {'lv': 21.19}},
                '1I21': {'agg': {'lv': 21.21}},
                '1I22': {'agg': {'lv': 21.22}},
                '1I23': {'agg': {'lv': 21.23}},
            }
        }
        area_mock = mock.Mock(data=data_mock, status=status_mock)
        instance = PowerQualityDataService(area_mock)

        actual_result = instance.compute('time_key')

        self.assertEqual(actual_result, {
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
                {'x': 21, 'y1': 11.21, 'y2': 21.21}
            ],
            'metrics': {
                'THI': {'sid': 2,
                        'value': 8.66,
                        'values': [{'x': 123, 'y': 5.42}, {'x': 123, 'y': 12.12}]},
                'THV': {'sid': 1,
                        'value': 2.16,
                        'values': [{'x': 123, 'y': 5.12}, {'x': 123, 'y': 4.54}]}
            },
            'order': ['THV', 'THI']
        })
