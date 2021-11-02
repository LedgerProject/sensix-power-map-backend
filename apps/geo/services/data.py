import logging
from typing import Optional

from apps.geo import choices
from apps.geo.models import GeohashArea

logger = logging.getLogger(__name__)


class BaseDataService(object):

    def __init__(self, area: GeohashArea) -> None:
        self.area = area

    def compute(self, time_range_key: str) -> dict:
        raise NotImplementedError


class PowerQualityDataService(BaseDataService):
    """
    Power quality data service, computes harmonic distortions from moving average area data.
    """
    VALUE_PRECISION = 2

    thd_metric_keys = ['THV', 'THI']

    hd_metrics_map = {
        3: {'voltage': ['1V3', '2V3', '3V3'], 'current': ['1I3', '2I3', '3I3']},
        5: {'voltage': ['1V5', '2V5', '3V5'], 'current': ['1I5', '2I5', '3I5']},
        7: {'voltage': ['1V7', '2V7', '3V7'], 'current': ['1I7', '2I7', '3I7']},
        9: {'voltage': ['1V9', '2V9', '3V9'], 'current': ['1I9', '2I9', '3I9']},
        11: {'voltage': ['1V11', '2V11', '3V11'], 'current': ['1I11', '2I11', '3I11']},
        13: {'voltage': ['1V13', '2V13', '3V13'], 'current': ['1I13', '2I13', '3I13']},
        15: {'voltage': ['1V15', '2V15', '3V15'], 'current': ['1I15', '2I15', '3I15']},
        17: {'voltage': ['1V17', '2V17', '3V17'], 'current': ['1I17', '2I17', '3I17']},
        19: {'voltage': ['1V19', '2V19', '3V19'], 'current': ['1I19', '2I19', '3I19']},
        21: {'voltage': ['1V21', '2V21', '3V21'], 'current': ['1I21', '2I21', '3I21']},
        23: {'voltage': ['1V23', '2V23', '3V23'], 'current': ['1I23', '2I23', '3I23']},
        25: {'voltage': ['1V25', '2V25', '3V25'], 'current': ['1I25', '2I25', '3I25']},
        27: {'voltage': ['1V27', '2V27', '3V27'], 'current': ['1I27', '2I27', '3I27']},
        29: {'voltage': ['1V29', '2V29', '3V29'], 'current': ['1I29', '2I29', '3I29']},
        31: {'voltage': ['1V31', '2V31', '3V31'], 'current': ['1I31', '2I31', '3I31']},
        33: {'voltage': ['1V33', '2V33', '3V33'], 'current': ['1I33', '2I33', '3I33']},
        35: {'voltage': ['1V35', '2V35', '3V35'], 'current': ['1I35', '2I35', '3I35']},
        37: {'voltage': ['1V37', '2V37', '3V37'], 'current': ['1I37', '2I37', '3I37']},
        39: {'voltage': ['1V39', '2V39', '3V39'], 'current': ['1I39', '2I39', '3I39']}
    }

    def compute(self, time_range_key: str) -> dict:
        status = self.area.status.get(time_range_key, {})
        data = self.area.data.get(time_range_key, {})

        thd_metrics_dict = {
            metric_key: {
                'sid': status.get(metric_key, {}).get('sid', choices.STATUS_NONE_ID),
                'value': data.get(metric_key, {}).get('agg', {}).get('lv'),
                'values': data.get(metric_key, {}).get('wins', []),
            } for metric_key in self.thd_metric_keys
        }

        harmonic_distortions = []
        for key, value in self.hd_metrics_map.items():
            avg_voltage_metric_value = self._get_average_agg_value_for(data, value.get('voltage'))
            avg_current_metric_value = self._get_average_agg_value_for(data, value.get('current'))

            harmonic_distortions.append({
                'x': key,
                'y1': avg_voltage_metric_value,
                'y2': avg_current_metric_value,
            })

        return {
            'sid': self._get_aggregated_status_id(time_range_key),
            'HDs': harmonic_distortions,
            'metrics': {**thd_metrics_dict},
            'order': [k for k in self.thd_metric_keys if k in data.keys()]
        }

    def _get_average_agg_value_for(self, data: dict, metric_keys: list) -> Optional[float]:
        avg = 0.0
        cnt = 0

        for metric_key in metric_keys:
            avg_value = data.get(metric_key, {}).get('agg', {}).get('avg')

            if avg_value is not None:
                avg += avg_value
                cnt += 1

        try:
            return round(avg / cnt, self.VALUE_PRECISION)
        except ZeroDivisionError:
            logger.warning(f'ZeroDivisionError while computing average agg of metric keys {metric_keys}')
            return None

    def _get_aggregated_status_id(self, time_range_key: str) -> int:
        status = self.area.status.get(time_range_key, {})

        try:
            status_id = min([status_object.get('sid', choices.STATUS_NONE_ID) for status_object in status.values()])
        except ValueError as e:
            status_id = choices.STATUS_NONE_ID

        return status_id


class PowerUsageDataService(BaseDataService):

    def compute(self, time_range_key: str) -> dict:
        return {}
