import coreapi

from apps.geo import choices


class GeohashAreaFields(object):
    coreapi_fields = (
        coreapi.Field(
            name='relative_time_range',
            location='query',
            required=False,
            description='Relative Time Range in hours. Options are: r3, r8, r24 or r48. Default is r3',
            type='string',
        ),
        coreapi.Field(
            name='category_id',
            location='query',
            required=False,
            description=f'Metric category Id. {dict(choices.CATEGORY_ID_CHOICES)}. Default is Power Quality.',
            type='integer',
        ),
    )
