from apps.geo import choices
from apps.geo.services.data import PowerQualityDataService, PowerUsageDataService

AGGREGATION_SERVICE_CLASS_MAP = {
    choices.CATEGORY_POWER_QUALITY_ID: PowerQualityDataService,
    choices.CATEGORY_POWER_USAGE_ID: PowerUsageDataService
}
