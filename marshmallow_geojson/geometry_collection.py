import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    GEOMETRY_COLLECTION,
)


class GeometryCollectionSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [GEOMETRY_COLLECTION],
            error='Invalid geometry collection type'),
    )
