from typing import Optional

from apps.geo import choices


class StatusService(object):
    status_keys_map = {
        'c': choices.STATUS_CRITICAL_ID,
        'w': choices.STATUS_WARNING_ID,
        'n': choices.STATUS_NORMAL_ID,
    }

    def __init__(self, thresholds: dict) -> None:
        self.thresholds = thresholds

    def update(self, value: Optional[float]) -> dict:
        updated_status = {
            'sid': choices.STATUS_NONE_ID,
        }

        if value is None:
            return updated_status

        for status_key in self.status_keys_map.keys():
            for threshold in self.thresholds.get(status_key, []):
                x1 = threshold.get('x1')
                x2 = threshold.get('x2')

                if x1 <= value <= x2:
                    updated_status['sid'] = self.status_keys_map.get(status_key)
                    updated_status['l'] = threshold.get('l')

                    return updated_status

        return updated_status
