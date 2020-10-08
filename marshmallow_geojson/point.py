from marshmallow.fields import (
    Tuple,
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    POINT,
)
from ._base import (
    BaseSchema,
    lon,
    lat,
)


class PointSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [POINT],
            error='Invalid point type'
        )
    )

    coordinates = Tuple(
        required=True,
        tuple_fields=(lon, lat),
    )
