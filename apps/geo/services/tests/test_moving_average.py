from django.test import TestCase

from apps.geo.services.moving_average import MovingAverageService


class MovingAverageServiceTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        super().setUp()

    def test__update_remove_old_windows(self):
        value = 66.66
        timestamp = 8000

        windows = [
            {'x': 1000, 'y': 1.1, 'min': 1.1, 'max': 1.1, 'cnt': 1},  # outside of relative time range
            {'x': 2000, 'y': 1.1, 'min': 1.1, 'max': 1.1, 'cnt': 1},  # outside of relative time range
            {'x': 3000, 'y': 1.1, 'min': 1.1, 'max': 1.1, 'cnt': 1},  # outside of relative time range
            {'x': 4000, 'y': 1.1, 'min': 1.1, 'max': 1.1, 'cnt': 1},  # outside of relative time range
            {'x': 5000, 'y': 1.1, 'min': 1.1, 'max': 1.1, 'cnt': 1},  # outside of relative time range
            {'x': 5001, 'y': 1.1, 'min': 1.1, 'max': 1.1, 'cnt': 1},
            {'x': 6000, 'y': 1.2, 'min': 1.2, 'max': 1.2, 'cnt': 1},
            {'x': 7000, 'y': 1.3, 'min': 1.3, 'max': 1.3, 'cnt': 1},
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=8000 - 5000, window_size=1000)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 5001, 'y': 1.1, 'min': 1.1, 'max': 1.1, 'cnt': 1},
                {'x': 6000, 'y': 1.2, 'min': 1.2, 'max': 1.2, 'cnt': 1},
                {'x': 7000, 'y': 1.3, 'min': 1.3, 'max': 1.3, 'cnt': 1},
                {'x': 8000, 'y': 66.66, 'min': 66.66, 'max': 66.66, 'cnt': 1}  # newly added
            ],
            'agg': {'cnt': 4, 'avg': 17.56, 'min': 1.1, 'max': 66.66, 'p2p': 65.56, 'r': 3000, 'w': 1000, 'lv': 66.66},
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_with_empty_data_input(self):
        value = 66.66
        timestamp = 1000

        data = {}

        instance = MovingAverageService(relative_time_range=1000, window_size=1000)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 1000, 'y': 66.66, 'min': 66.66, 'max': 66.66, 'cnt': 1}  # newly added
            ],
            'agg': {'cnt': 1, 'avg': 66.66, 'min': 66.66, 'max': 66.66, 'p2p': 0.0, 'r': 1000, 'w': 1000, 'lv': 66.66},
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_add_new_window_to_windows(self):
        value = 66.66
        timestamp = 6000

        windows = [
            {'x': 1000, 'y': 11.1, 'min': 11.1, 'max': 11.1, 'cnt': 1},  # outside of relative time range
            {'x': 2000, 'y': 11.1, 'min': 11.1, 'max': 11.1, 'cnt': 1},  # outside of relative time range
            {'x': 3001, 'y': 11.1, 'min': 11.1, 'max': 11.1, 'cnt': 1},
            {'x': 4000, 'y': 11.2, 'min': 11.2, 'max': 11.2, 'cnt': 1},
            {'x': 5000, 'y': 11.3, 'min': 11.3, 'max': 11.3, 'cnt': 1},
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=6000 - 3000, window_size=1000)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 3001, 'y': 11.1, 'min': 11.1, 'max': 11.1, 'cnt': 1},
                {'x': 4000, 'y': 11.2, 'min': 11.2, 'max': 11.2, 'cnt': 1},
                {'x': 5000, 'y': 11.3, 'min': 11.3, 'max': 11.3, 'cnt': 1},
                {'x': 6000, 'y': 66.66, 'min': 66.66, 'max': 66.66, 'cnt': 1}
            ],
            'agg': {'cnt': 4, 'avg': 25.06, 'min': 11.1, 'max': 66.66, 'p2p': 55.56, 'r': 3000, 'w': 1000, 'lv': 66.66},
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_add_last_window(self):
        value = 11.22
        timestamp = 4250

        windows = [
            {'x': 1000, 'y': 11.1, 'min': 11.1, 'max': 11.1, 'cnt': 1},  # outside of relative time range
            {'x': 2000, 'y': 11.1, 'min': 10.2, 'max': 11.1, 'cnt': 2},  # outside of relative time range
            {'x': 3001, 'y': 11.1, 'min': 10.2, 'max': 11.5, 'cnt': 3},
            {'x': 4000, 'y': 11.2, 'min': 11.2, 'max': 11.2, 'cnt': 1},
            {'x': 4001, 'y': 11.3, 'min': 10.2, 'max': 11.3, 'cnt': 2},  # inside current window (left edge)
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=4250 - 3000, window_size=250)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 3001, 'y': 11.1, 'min': 10.2, 'max': 11.5, 'cnt': 3},
                {'x': 4000, 'y': 11.2, 'min': 11.2, 'max': 11.2, 'cnt': 1},
                {'x': 4001, 'y': 11.27, 'min': 10.2, 'max': 11.3, 'cnt': 3}  # keeps the window initial timestamp
            ],
            'agg': {'cnt': 7, 'avg': 11.19, 'min': 10.2, 'max': 11.5, 'p2p': 1.3, 'r': 1250, 'w': 250, 'lv': 11.22},
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_with_precision1(self):
        value = 11.22
        timestamp = 4250

        windows = [
            {'x': 3001, 'y': 11.111, 'min': 10.212, 'max': 11.555, 'cnt': 3},
            {'x': 4000, 'y': 11.223, 'min': 11.212, 'max': 11.231, 'cnt': 1},
            {'x': 4250, 'y': 11.333, 'min': 10.211, 'max': 11.398, 'cnt': 2},  # inside current window (right edge)
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=4250 - 3000, window_size=250, precision=1)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 3001, 'y': 11.111, 'min': 10.212, 'max': 11.555, 'cnt': 3},
                {'x': 4000, 'y': 11.223, 'min': 11.212, 'max': 11.231, 'cnt': 1},
                {'x': 4250, 'y': 11.3, 'min': 10.2, 'max': 11.4, 'cnt': 3}  # will update new precision for last window
            ],
            'agg': {'cnt': 7, 'avg': 11.2, 'min': 10.2, 'max': 11.6, 'p2p': 1.4, 'r': 1250, 'w': 250, 'lv': 11.22},
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_with_precision3(self):
        value = 11.22
        timestamp = 4250

        windows = [
            {'x': 3001, 'y': 11.111, 'min': 10.212, 'max': 11.555, 'cnt': 3},
            {'x': 4000, 'y': 11.223, 'min': 11.212, 'max': 11.231, 'cnt': 1},
            {'x': 4250, 'y': 11.333, 'min': 10.211, 'max': 11.398, 'cnt': 2},  # inside current window (right edge)
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=4250 - 3000, window_size=250, precision=3)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 3001, 'y': 11.111, 'min': 10.212, 'max': 11.555, 'cnt': 3},
                {'x': 4000, 'y': 11.223, 'min': 11.212, 'max': 11.231, 'cnt': 1},
                {'x': 4250, 'y': 11.295, 'min': 10.211, 'max': 11.398, 'cnt': 3}
            ],
            'agg': {
                'cnt': 7, 'avg': 11.206, 'min': 10.211, 'max': 11.555, 'p2p': 1.344, 'r': 1250, 'w': 250, 'lv': 11.22
            },
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_window_and_agg_min(self):
        value = 10.2
        timestamp = 4250

        windows = [
            {'x': 3001, 'y': 11.11, 'min': 10.21, 'max': 11.55, 'cnt': 3},
            {'x': 4000, 'y': 11.22, 'min': 11.21, 'max': 11.23, 'cnt': 1},
            {'x': 4250, 'y': 11.33, 'min': 10.21, 'max': 11.39, 'cnt': 2},  # inside current window (right edge)
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=4250 - 3000, window_size=250)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 3001, 'y': 11.11, 'min': 10.21, 'max': 11.55, 'cnt': 3},
                {'x': 4000, 'y': 11.22, 'min': 11.21, 'max': 11.23, 'cnt': 1},
                {'x': 4250, 'y': 10.95, 'min': 10.2, 'max': 11.39, 'cnt': 3}
            ],
            'agg': {'cnt': 7, 'avg': 11.06, 'min': 10.2, 'max': 11.55, 'p2p': 1.35, 'r': 1250, 'w': 250, 'lv': 10.2},
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_window_and_agg_max(self):
        value = 11.6
        timestamp = 4250

        windows = [
            {'x': 3001, 'y': 11.11, 'min': 10.21, 'max': 11.55, 'cnt': 3},
            {'x': 4000, 'y': 11.22, 'min': 11.21, 'max': 11.23, 'cnt': 1},
            {'x': 4250, 'y': 11.33, 'min': 10.21, 'max': 11.39, 'cnt': 2},  # inside current window (right edge)
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=4250 - 3000, window_size=250)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 3001, 'y': 11.11, 'min': 10.21, 'max': 11.55, 'cnt': 3},
                {'x': 4000, 'y': 11.22, 'min': 11.21, 'max': 11.23, 'cnt': 1},
                {'x': 4250, 'y': 11.42, 'min': 10.21, 'max': 11.6, 'cnt': 3}
            ],
            'agg': {'cnt': 7, 'avg': 11.26, 'min': 10.21, 'max': 11.6, 'p2p': 1.39, 'r': 1250, 'w': 250, 'lv': 11.6},
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_window_min(self):
        value = 10.2
        timestamp = 4250

        windows = [
            {'x': 3001, 'y': 11.11, 'min': 9.21, 'max': 11.55, 'cnt': 3},
            {'x': 4000, 'y': 11.22, 'min': 11.21, 'max': 11.23, 'cnt': 1},
            {'x': 4250, 'y': 11.33, 'min': 10.21, 'max': 11.39, 'cnt': 2},  # inside current window (right edge)
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=4250 - 3000, window_size=250)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 3001, 'y': 11.11, 'min': 9.21, 'max': 11.55, 'cnt': 3},
                {'x': 4000, 'y': 11.22, 'min': 11.21, 'max': 11.23, 'cnt': 1},
                {'x': 4250, 'y': 10.95, 'min': 10.2, 'max': 11.39, 'cnt': 3}
            ],
            'agg': {'cnt': 7, 'avg': 11.06, 'min': 9.21, 'max': 11.55, 'p2p': 2.34, 'r': 1250, 'w': 250, 'lv': 10.2},
        }

        self.assertEqual(actual_result, expected_result)

    def test__update_window_max(self):
        value = 11.4
        timestamp = 4250

        windows = [
            {'x': 3001, 'y': 11.11, 'min': 10.21, 'max': 11.55, 'cnt': 3},
            {'x': 4000, 'y': 11.22, 'min': 11.21, 'max': 11.23, 'cnt': 1},
            {'x': 4250, 'y': 11.33, 'min': 10.21, 'max': 11.39, 'cnt': 2},  # inside current window (right edge)
        ]
        data = {'wins': windows}

        instance = MovingAverageService(relative_time_range=4250 - 3000, window_size=250)
        actual_result = instance.update(value, timestamp, data)

        expected_result = {
            'wins': [
                {'x': 3001, 'y': 11.11, 'min': 10.21, 'max': 11.55, 'cnt': 3},
                {'x': 4000, 'y': 11.22, 'min': 11.21, 'max': 11.23, 'cnt': 1},
                {'x': 4250, 'y': 11.35, 'min': 10.21, 'max': 11.4, 'cnt': 3}
            ],
            'agg': {'cnt': 7, 'avg': 11.23, 'min': 10.21, 'max': 11.55, 'p2p': 1.34, 'r': 1250, 'w': 250, 'lv': 11.4},
        }

        self.assertEqual(actual_result, expected_result)
