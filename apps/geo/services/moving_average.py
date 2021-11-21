"""
Service utils to compute moving average for live cells data.
"""
import sys


class MovingAverageService(object):
    """
    Calculates moving average (moving mean) values within a relative time range.
    e.g. 3 * 60 * 60 = last 3 hours.

    Input:
      - relative time range in seconds
      - window size in seconds
      - new value usually just received from a device
      - data to be updated for new value

    Data structure:
    {
        'wins': [
            # Each object represents a window, aggregating all values received within this window.
            {
               'x': 1605475447,  # last epoch timestamp for this window
               'y': 3.3,  # average value for this window
               'min': 1.1,  # minimum value for this window
               'max': 3.1,  # maximum value for this window
               'cnt': 1,  # number of values aggregated to this window
            },
            { ... },
            { ... },
            { ... },
        ],
        'agg': {
            'avg': 11.12,  # average value for all windows
            'min': 1.22,  # minimum value for all windows
            'max': 21.2,  # maximum value for all windows
            'p2p': 19.98,  # peak to peak value for all windows
            'lv': 32.22,  # last value from last window
            'cnt': 11,  # number of windows considered to compute avg / min / max
        }
    }
    """

    def __init__(self, relative_time_range: int, window_size: int, precision: int = 2) -> None:
        """
        Initializing.
        Use window_size=0 to have a separate window for every new value. Essentially bypassing the aggregation.

        :param relative_time_range: the relative time range in seconds
        :param window_size: the window size in seconds. A window size of 0, will result in new windows for every value.
        :param precision: number of decimals.
        """
        self.relative_time_range = relative_time_range
        self.window_size = window_size
        self.precision = precision

    def update(self, value: float, timestamp: int, data: dict) -> dict:
        """
        Update given data dict for the new value received.
        Will update last window or add new window depending on timestamp.
        Will remove windows outside of the relative time range.

        :param value the new value
        :param timestamp the epoch timestamp of the new value
        :param data existing dict of windows and aggregates to be updated

        :return updated data dict with windows and aggregates.
        """
        if value is None:
            return data  # just return untouched data

        windows = data.get('wins', [])

        windows = self._compute_windows(value, timestamp, windows)
        aggregates = self._compute_windows_aggregates(windows, value)

        return {
            'wins': windows,
            'agg': aggregates,
        }

    def _compute_windows(self, value: float, timestamp: int, windows: list):
        windows = self._remove_old_windows(timestamp, windows)
        value = round(value, self.precision)

        window = {
            'x': timestamp,
            'y': value,
            'min': value,
            'max': value,
            'cnt': 1,
        }

        has_no_windows = not bool(windows)
        if has_no_windows:
            windows.append(window)
            return windows

        should_update_last_window = self._should_update_last_window(timestamp, windows)

        if should_update_last_window:
            windows = self._update_last_window(value, windows)
        else:
            windows.append(window)

        return windows

    def _should_update_last_window(self, timestamp: int, windows: list):
        last_window = windows[-1]
        is_within_current_window = last_window.get('x') > (timestamp - self.window_size)
        return is_within_current_window

    def _update_last_window(self, value: float, windows: list):
        last_window = windows[-1]

        last_window_cnt = last_window.get('cnt')
        last_window_min = last_window.get('min')
        last_window_max = last_window.get('max')
        agg_new_value = (last_window.get('y') * last_window_cnt + value) / (last_window_cnt + 1)

        last_window.update({
            'y': round(agg_new_value, self.precision),
            'min': round(value if last_window_min > value else last_window_min, self.precision),
            'max': round(value if last_window_max < value else last_window_max, self.precision),
            'cnt': last_window_cnt + 1,
        })

        return windows

    def _remove_old_windows(self, timestamp: int, windows: list):
        windows = [
            v for v in windows if v.get('x', 0) > (timestamp - self.relative_time_range)
        ]
        return windows

    def _compute_windows_aggregates(self, windows: list, last_value: float):
        cnt_value = sum([w.get('cnt') for w in windows])
        sum_value = 0
        min_value = sys.maxsize
        max_value = -sys.maxsize

        for win in windows:
            value = win.get('y')
            weight = win.get('cnt')

            sum_value += value * weight

            if win.get('min') < min_value:
                min_value = win.get('min')

            if win.get('max') > max_value:
                max_value = win.get('max')

        return {
            'cnt': cnt_value,
            'avg': round(sum_value / cnt_value, self.precision),
            'min': round(min_value, self.precision),
            'max': round(max_value, self.precision),
            'p2p': round(max_value - min_value, self.precision),
            'r': self.relative_time_range,
            'w': self.window_size,
            'lv': last_value,
        }
