import itertools
import logging
from collections import OrderedDict
from typing import Optional

from django.conf import settings

from apps.geo import choices
from apps.geo.models import GeohashArea
from apps.geo.services.status import StatusService

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
    composite_metric_keys = settings.CATEGORY_METRIC_KEYS_MAP[choices.CATEGORY_POWER_QUALITY_ID]

    hd_metric_keys_map = {
        3: [['1V3', '2V3', '3V3'], ['1I3', '2I3', '3I3']],
        5: [['1V5', '2V5', '3V5'], ['1I5', '2I5', '3I5']],
        7: [['1V7', '2V7', '3V7'], ['1I7', '2I7', '3I7']],
        9: [['1V9', '2V9', '3V9'], ['1I9', '2I9', '3I9']],
        11: [['1V11', '2V11', '3V11'], ['1I11', '2I11', '3I11']],
        13: [['1V13', '2V13', '3V13'], ['1I13', '2I13', '3I13']],
        15: [['1V15', '2V15', '3V15'], ['1I15', '2I15', '3I15']],
        17: [['1V17', '2V17', '3V17'], ['1I17', '2I17', '3I17']],
        19: [['1V19', '2V19', '3V19'], ['1I19', '2I19', '3I19']],
        21: [['1V21', '2V21', '3V21'], ['1I21', '2I21', '3I21']],
        23: [['1V23', '2V23', '3V23'], ['1I23', '2I23', '3I23']],
        25: [['1V25', '2V25', '3V25'], ['1I25', '2I25', '3I25']],
        27: [['1V27', '2V27', '3V27'], ['1I27', '2I27', '3I27']],
        29: [['1V29', '2V29', '3V29'], ['1I29', '2I29', '3I29']],
        31: [['1V31', '2V31', '3V31'], ['1I31', '2I31', '3I31']],
        33: [['1V33', '2V33', '3V33'], ['1I33', '2I33', '3I33']],
        35: [['1V35', '2V35', '3V35'], ['1I35', '2I35', '3I35']],
        37: [['1V37', '2V37', '3V37'], ['1I37', '2I37', '3I37']],
        39: [['1V39', '2V39', '3V39'], ['1I39', '2I39', '3I39']]
    }

    def compute(self, time_range_key: str) -> dict:
        return {
            'sid': self._get_agg_sid(time_range_key, self.composite_metric_keys),
            'labels': self._get_labels_for(time_range_key),
            'HDs': self._get_harmonic_distortions_list_for(time_range_key),
            'metrics': self._get_thd_metrics_dict_for(time_range_key),
            'order': [
                settings.THD_AGG_VOLTAGE_METRIC_KEY,
                settings.THD_AGG_CURRENT_METRIC_KEY
            ],
        }

    def _get_harmonic_distortions_list_for(self, time_range_key: str) -> list:
        harmonic_distortions = []
        for order, hd_metric_keys in self.hd_metric_keys_map.items():
            voltage_metric_keys = hd_metric_keys[0]
            current_metric_keys = hd_metric_keys[1]

            avg_voltage_metric_value = self._get_agg_value_for(time_range_key, voltage_metric_keys)
            avg_current_metric_value = self._get_agg_value_for(time_range_key, current_metric_keys)

            harmonic_distortions.append({
                'x': order,
                'y1': avg_voltage_metric_value,
                'y2': avg_current_metric_value,
            })
        return harmonic_distortions

    def _get_thd_metrics_dict_for(self, time_range_key: str) -> dict:
        return {
            settings.THD_AGG_VOLTAGE_METRIC_KEY: self._get_thd_metric_dict_for(
                time_range_key, settings.THD_VOLTAGE_METRIC_KEYS
            ),
            settings.THD_AGG_CURRENT_METRIC_KEY: self._get_thd_metric_dict_for(
                time_range_key, settings.THD_CURRENT_METRIC_KEYS
            )
        }

    def _get_thd_metric_dict_for(self, time_range_key: str, metric_keys: list) -> dict:
        return {
            'sid': self._get_agg_sid(time_range_key, metric_keys),
            'value': self._get_agg_value_for(time_range_key, metric_keys),
            'values': self._get_agg_values_for(time_range_key, metric_keys)
        }

    def _get_agg_sid(self, time_range_key: str, metric_keys: list) -> int:
        status = self.area.status.get(time_range_key, {})
        status_ids = [status.get(k, {}).get('sid', choices.STATUS_NONE_ID) for k in metric_keys]

        return StatusService.get_agg_status(status_ids)

    def _get_agg_value_for(self, time_range_key: str, metric_keys: list) -> Optional[float]:
        data = self.area.data.get(time_range_key, {})
        avg = 0.0
        cnt = 0

        for metric_key in metric_keys:
            avg_value = data.get(metric_key, {}).get('agg', {}).get('avg')

            if avg_value is not None:
                avg += avg_value
                cnt += 1

        try:
            return round(avg / cnt, settings.VALUE_PRECISION)
        except ZeroDivisionError:
            logger.warning(f'ZeroDivisionError while computing average agg of metric keys {metric_keys}')
            return None

    def _get_agg_values_for(self, time_range_key: str, metric_keys: list) -> list:
        """
        Aggregate `wins` by index, considering latest timestamp of a group.
        :return: moving average windows aka `wins` as list of dicts.
        """
        data = self.area.data.get(time_range_key, {})
        wins_length = max([len(data.get(k, {}).get('wins', [])) for k in metric_keys])

        values = []
        for index in range(-wins_length, 0):
            start = index
            end = index + 1 or None

            wins_for_index = [data.get(k, {}).get('wins', [])[start:end] for k in metric_keys]
            wins_for_index = list(itertools.chain.from_iterable(wins_for_index))

            if not wins_for_index:
                continue

            values.append({
                'x': max([w.get('x') for w in wins_for_index]),
                'y': round(sum([w.get('y') for w in wins_for_index]) / len(wins_for_index), settings.VALUE_PRECISION),
                'cnt': max([w.get('cnt') for w in wins_for_index]),
                'max': max([w.get('max') for w in wins_for_index]),
                'min': min([w.get('min') for w in wins_for_index]),
            })

        return values

    def _get_labels_for(self, time_range_key: str) -> list:
        status = self.area.status.get(time_range_key, {})

        desired_states = [choices.STATUS_CRITICAL_ID, choices.STATUS_WARNING_ID]

        labels = [
            status.get(k, {})
            for k in self.composite_metric_keys
            if status.get(k, {}).get('l')
        ]

        labels.sort(key=lambda o: o.get('sid'))

        return list(OrderedDict.fromkeys([
            o.get('l') for o in labels if o.get('sid') in desired_states
        ]))


class PowerUsageDataService(BaseDataService):

    def compute(self, time_range_key: str) -> dict:
        return {}
