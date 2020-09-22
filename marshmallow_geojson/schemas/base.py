from enum import Enum
import marshmallow as ma
from marshmallow.validate import (
    Range,
    OneOf,
)
from marshmallow.fields import (
    Float,
    Str,
)


class GeometryType(Enum):
    """
    geometry type
    """
    point = 'Point'
    multi_point = 'MultiPoint'
    line_string = 'LineString'
    multi_line_string = 'MultiLineString'
    polygon = 'Polygon'
    multi_polygon = 'MultiPolygon'
    geometry_collection = 'GeometryCollection'


class Coordinates(ma.Schema):
    latitude = Float(
        required=True,
        validate=Range(
            min=-90,
            max=90,
            error='Latitude must be between -90, 90'),
    )

    longitude = Float(
        required=True,
        validate=Range(
            min=-180,
            max=180,
            error='Longitude must be between -180, 180'),
    )


class BaseSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [json_type.value for json_type in GeometryType],
            error='Unavailable GeoJSON type'),
    )
