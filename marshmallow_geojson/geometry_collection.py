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


class GeometryCollectionSchema(BaseSchema):
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
