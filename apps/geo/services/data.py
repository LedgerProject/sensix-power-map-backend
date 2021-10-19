from copy import deepcopy

from apps.geo import choices
from apps.geo.models import GeohashArea


class BaseDataService(object):

    def __init__(self, area: GeohashArea) -> None:
        self.area = area

    def compute(self, time_range_key: str) -> dict:
        raise NotImplementedError


class PowerQualityDataService(BaseDataService):
    """
    Power quality data service, computes harmonic distortions from moving average area data.
    """
    thd_metric_keys = ['THV', 'THI']

    hd_metrics_map = {
        3: {'voltage': '1V3', 'current': '1I3'},
        5: {'voltage': '1V5', 'current': '1I5'},
        7: {'voltage': '1V7', 'current': '1I7'},
        9: {'voltage': '1V9', 'current': '1I9'},
        11: {'voltage': '1V11', 'current': '1I11'},
        13: {'voltage': '1V13', 'current': '1I13'},
        15: {'voltage': '1V15', 'current': '1I15'},
        17: {'voltage': '1V17', 'current': '1I17'},
        19: {'voltage': '1V19', 'current': '1I19'},
        21: {'voltage': '1V21', 'current': '1I21'}
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
            voltage_metric_value = data.get(value.get('voltage'), {}).get('agg', {}).get('lv')
            current_metric_value = data.get(value.get('current'), {}).get('agg', {}).get('lv')

            harmonic_distortions.append({
                'x': key,
                'y1': voltage_metric_value,
                'y2': current_metric_value,
            })

        return {
            'HDs': harmonic_distortions,
            'metrics': {**thd_metrics_dict},
            'order': [k for k in self.thd_metric_keys if k in data.keys()]
        }


class PowerUsageDataService(BaseDataService):

    def compute(self, time_range_key: str) -> dict:
        return {}
