# ID order is important, we use it for ordering ASC
STATUS_CRITICAL_ID = 0
STATUS_WARNING_ID = 1
STATUS_NORMAL_ID = 2
STATUS_NONE_ID = 3

STATUS_ID_CHOICES = (
    (STATUS_CRITICAL_ID, 'Critical'),
    (STATUS_WARNING_ID, 'Warning'),
    (STATUS_NORMAL_ID, 'Optimal'),
    (STATUS_NONE_ID, 'None'),
)