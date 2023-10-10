from __future__ import annotations

from marshmallow.fields import List, Nested, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .examples import GEOJSON_GEOMETRY_COLLECTION
from .geometry import GeometriesSchema
from .object_type import GEOMETRY_COLLECTION


class GeometryCollectionSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [GEOMETRY_COLLECTION],
            error='Invalid geometry collection type',
        )
    )

    geometries = List(
        Nested(GeometriesSchema()),
        required=True,
        metadata=dict(example=GEOJSON_GEOMETRY_COLLECTION["geometries"]),
    )
    )
