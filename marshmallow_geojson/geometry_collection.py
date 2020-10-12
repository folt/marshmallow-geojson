from marshmallow.fields import (
    Tuple,
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    GEOMETRY_COLLECTION,
)
from ._base import (
    BaseSchema,
    lon,
    lat,
)


class GeometryCollectionSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [GEOMETRY_COLLECTION],
            error='Invalid geometry collection type',
        )
    )

    coordinates = Tuple(
        required=True,
        tuple_fields=(lon, lat),
    )

