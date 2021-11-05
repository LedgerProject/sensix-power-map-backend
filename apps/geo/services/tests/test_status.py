from django.test import TestCase

from apps.geo.choices import STATUS_NONE_ID, STATUS_NORMAL_ID, STATUS_WARNING_ID, STATUS_CRITICAL_ID
from apps.geo.services.status import StatusService


class StatusServiceTestCase(TestCase):
    maxDiff = None

    thresholds_mock = {
        "c": [
            {
                "x1": 0.1,
                "x2": 0.65,
                "l": "Critical Text 1"
            },
            {
                "x1": -0.65,
                "x2": -0.1,
                "l": "Critical Text 2"
            }
        ],
        "w": [
            {
                "x1": 0.65,
                "x2": 0.9,
                "l": "Warning Text 1"
            },
            {
                "x1": -0.9,
                "x2": -0.65,
                "l": "Warning Text 2"
            },
            {
                "x1": -0.1,
                "x2": 0.1,
                "l": "Warning Text 3"
            },
        ],
        "n": [
            {
                "x1": 0.9,
                "x2": 1.0,
                "l": "Normal Text 1"
            },
            {
                "x1": -1.0,
                "x2": -0.9,
                "l": "Normal Text 2"
            }
        ]
    }

    def setUp(self):
        super().setUp()

    def test__update_none(self):
        instance = StatusService(self.thresholds_mock)

        # outside of [-1, 1] threshold interval range.
        self.assertEqual(instance.update(1.0000000001), {'sid': STATUS_NONE_ID})
        self.assertEqual(instance.update(2.22), {'sid': STATUS_NONE_ID})
        self.assertEqual(instance.update(-1.01), {'sid': STATUS_NONE_ID})

    def test__update_nominal(self):
        instance = StatusService(self.thresholds_mock)

        # inside of (0.9, 1] | [-1, -0.9) threshold interval range.
        self.assertEqual(instance.update(1), {'sid': STATUS_NORMAL_ID, 'l': 'Normal Text 1'})
        self.assertEqual(instance.update(0.95), {'sid': STATUS_NORMAL_ID, 'l': 'Normal Text 1'})
        self.assertEqual(instance.update(0.91), {'sid': STATUS_NORMAL_ID, 'l': 'Normal Text 1'})

        self.assertEqual(instance.update(-1), {'sid': STATUS_NORMAL_ID, 'l': 'Normal Text 2'})
        self.assertEqual(instance.update(-0.95), {'sid': STATUS_NORMAL_ID, 'l': 'Normal Text 2'})
        self.assertEqual(instance.update(-0.91), {'sid': STATUS_NORMAL_ID, 'l': 'Normal Text 2'})

    def test__update_warning(self):
        instance = StatusService(self.thresholds_mock)

        # inside of (0.65, 0.9] | [-0.9, 0.65) | (-0.1, 0.1) threshold interval range.
        self.assertEqual(instance.update(0.66), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 1'})
        self.assertEqual(instance.update(0.75), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 1'})
        self.assertEqual(instance.update(0.9), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 1'})

        self.assertEqual(instance.update(-0.66), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 2'})
        self.assertEqual(instance.update(-0.75), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 2'})
        self.assertEqual(instance.update(-0.9), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 2'})

        self.assertEqual(instance.update(-0.09), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 3'})
        self.assertEqual(instance.update(0.0), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 3'})
        self.assertEqual(instance.update(0.09), {'sid': STATUS_WARNING_ID, 'l': 'Warning Text 3'})

    def test__update_critical(self):
        instance = StatusService(self.thresholds_mock)

        # inside of [0.1, 0.65] | [-0.65, -0.1] threshold interval range.
        self.assertEqual(instance.update(0.1), {'sid': STATUS_CRITICAL_ID, 'l': 'Critical Text 1'})
        self.assertEqual(instance.update(0.49), {'sid': STATUS_CRITICAL_ID, 'l': 'Critical Text 1'})
        self.assertEqual(instance.update(0.65), {'sid': STATUS_CRITICAL_ID, 'l': 'Critical Text 1'})

        self.assertEqual(instance.update(-0.1), {'sid': STATUS_CRITICAL_ID, 'l': 'Critical Text 2'})
        self.assertEqual(instance.update(-0.49), {'sid': STATUS_CRITICAL_ID, 'l': 'Critical Text 2'})
        self.assertEqual(instance.update(-0.65), {'sid': STATUS_CRITICAL_ID, 'l': 'Critical Text 2'})

    def test__get_agg_status(self):
        self.assertEqual(StatusService.get_agg_status(
            [STATUS_WARNING_ID, STATUS_CRITICAL_ID, STATUS_NORMAL_ID, STATUS_NONE_ID]
        ), STATUS_CRITICAL_ID)
        self.assertEqual(StatusService.get_agg_status(
            [STATUS_CRITICAL_ID, STATUS_CRITICAL_ID, STATUS_NONE_ID]
        ), STATUS_CRITICAL_ID)
        self.assertEqual(StatusService.get_agg_status(
            [STATUS_WARNING_ID, STATUS_WARNING_ID, STATUS_NORMAL_ID]
        ), STATUS_WARNING_ID)
        self.assertEqual(StatusService.get_agg_status(
            [STATUS_NONE_ID, STATUS_WARNING_ID, STATUS_NORMAL_ID]
        ), STATUS_WARNING_ID)
        self.assertEqual(StatusService.get_agg_status(
            [STATUS_NONE_ID, STATUS_NONE_ID, STATUS_NORMAL_ID]
        ), STATUS_NORMAL_ID)
        self.assertEqual(StatusService.get_agg_status(
            [STATUS_NONE_ID, STATUS_NONE_ID]
        ), STATUS_NONE_ID)
        self.assertEqual(StatusService.get_agg_status(
            []
        ), STATUS_NONE_ID)