"""Properties schema for GeoJSON Feature objects."""

from __future__ import annotations

from ._base import BaseSchema


class PropertiesSchema(BaseSchema):
    """Base schema for Feature properties.

    This schema serves as a base class for custom property schemas. Users
    should subclass this schema to define their own property structures
    for Feature objects.

    According to RFC 7946 Section 3.2, a Feature object has a "properties"
    member which is a JSON object (or JSON null value) containing feature
    properties.

    By default, this schema accepts any fields (unknown='include') to allow
    arbitrary properties as per GeoJSON specification.

    Example:
        To create a custom properties schema::

            from marshmallow.fields import Str, Number
            from marshmallow_geojson import PropertiesSchema

            class MyPropertiesSchema(PropertiesSchema):
                name = Str(required=True)
                population = Number(required=False)

    References:
        https://www.rfc-editor.org/rfc/rfc7946.html#section-3.2
    """

    class Meta:
        unknown = "include"
