from marshmallow.fields import (
    Nested,
    List,
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    GEOMETRY_COLLECTION,
)
from ._base import BaseSchema
from .geometry import GeometriesSchema

from .point import PointSchema
from .multi_polygon import MultiPolygonSchema
from .line_string import LineStringSchema
from .multi_line_string import MultiLineStringSchema
from .polygon import PolygonSchema
from .multi_point import MultiPointSchema


class GeometryCollectionSchema(BaseSchema):
    point_schema = PointSchema
    multi_point_schema = MultiPointSchema
    line_string_schema = LineStringSchema
    multi_line_string_schema = MultiLineStringSchema
    polygon_schema = PolygonSchema
    multi_polygon_schema = MultiPolygonSchema

    type = Str(
        required=True,
        validate=OneOf(
            [GEOMETRY_COLLECTION],
            error='Invalid geometry collection type',
        )
    )

    geometries = List(
        Nested(GeometriesSchema),
        required=True,
    )
