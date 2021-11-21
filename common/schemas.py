"""
Common Schemas.
"""
from rest_framework.permissions import AllowAny
from rest_framework.renderers import CoreJSONRenderer
from rest_framework.schemas import AutoSchema
from rest_framework.schemas import get_schema_view
from rest_framework_swagger import renderers


class CustomSchema(AutoSchema):
    def get_link(self, path, method, base_url):
        link = super().get_link(path, method, base_url)
        link._fields += self.get_core_fields(method)
        return link

    def get_core_fields(self, method):
        coreapi_fields = getattr(self.view, 'coreapi_fields', ())

        if method in ['POST', 'PATCH', 'PUT']:
            return tuple([field for field in coreapi_fields if field.location in ['form', 'body']])

        if method in ['GET', 'DELETE']:
            return tuple([field for field in coreapi_fields if field.location in ['path', 'query']])

        return coreapi_fields


main_swagger_schema_view = get_schema_view(
    title="REST API Docs", description='Users Management Service',
    renderer_classes=[
        CoreJSONRenderer,
        renderers.OpenAPIRenderer,
        renderers.SwaggerUIRenderer
    ],
    permission_classes=[AllowAny])
