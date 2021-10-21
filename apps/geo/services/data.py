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
        21: {'voltage': '1V21', 'current': '1I21'},
        23: {'voltage': '1V23', 'current': '1I23'},
        25: {'voltage': '1V25', 'current': '1I25'},
        27: {'voltage': '1V27', 'current': '1I27'},
        29: {'voltage': '1V29', 'current': '1I29'},
        31: {'voltage': '1V31', 'current': '1I31'},
        33: {'voltage': '1V33', 'current': '1I33'},
        35: {'voltage': '1V35', 'current': '1I35'},
        37: {'voltage': '1V37', 'current': '1I37'},
        39: {'voltage': '1V39', 'current': '1I39'}
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
            'sid': self._get_aggregated_status_id(time_range_key),
            'HDs': harmonic_distortions,
            'metrics': {**thd_metrics_dict},
            'order': [k for k in self.thd_metric_keys if k in data.keys()]
        }

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
