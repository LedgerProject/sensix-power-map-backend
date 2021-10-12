from django.contrib import admin
from django.contrib.admin import register
from django.contrib.postgres.fields import JSONField
from django_json_widget.widgets import JSONEditorWidget

from apps.geo.models import GeohashArea


@register(GeohashArea)
class GeohashAreaAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget()},
    }
