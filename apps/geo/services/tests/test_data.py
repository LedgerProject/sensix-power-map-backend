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
                '1V7': {
                    'sid': choices.STATUS_WARNING_ID,
                    'l': 'HD7 I Some text'
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
                '1V23': {'agg': {'lv': 11.23}},
                '1V25': {'agg': {'lv': 11.25}},
                '1V27': {'agg': {'lv': 11.27}},
                '1V29': {'agg': {'lv': 11.29}},
                '1V31': {'agg': {'lv': 11.31}},
                '1V33': {'agg': {'lv': 11.33}},
                '1V35': {'agg': {'lv': 11.35}},
                '1V37': {'agg': {'lv': 11.37}},
                '1V39': {'agg': {'lv': 11.39}},
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
                '1I23': {'agg': {'lv': 21.23}},
                '1I25': {'agg': {'lv': 21.25}},
                '1I27': {'agg': {'lv': 21.27}},
                '1I29': {'agg': {'lv': 21.29}},
                '1I31': {'agg': {'lv': 21.31}},
                '1I33': {'agg': {'lv': 21.33}},
                '1I35': {'agg': {'lv': 21.35}},
                '1I37': {'agg': {'lv': 21.37}},
                '1I39': {'agg': {'lv': 21.39}},
                'will_ignore': {'agg': {'lv': 66.66}},
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
                'THI': {'sid': 2,
                        'value': 8.66,
                        'values': [{'x': 123, 'y': 5.42}, {'x': 123, 'y': 12.12}]},
                'THV': {'sid': 1,
                        'value': 2.16,
                        'values': [{'x': 123, 'y': 5.12}, {'x': 123, 'y': 4.54}]}
            },
            'order': ['THV', 'THI']
        })
