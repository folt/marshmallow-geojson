import marshmallow as ma

from marshmallow.validate import (
    OneOf,
)
from marshmallow.fields import (
    Str,
)

from .schemas import (
    GeometryType,
)


class GeoJSONType(GeometryType):
    """
    GeoJSON types
    https://www.rfc-editor.org/rfc/rfc7946.html#section-1.4
    """
    feature = 'Feature'
    feature_collection = 'FeatureCollection'


class GeoJSON(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [json_type.value for json_type in GeoJSONType],
            error='Unavailable GeoJSON type'),
    )
