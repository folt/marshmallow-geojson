import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .element import (
    CoordinateField,
)
from .object_type import (
    POINT,
)


class PointSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [POINT],
            error='Invalid point type'),
    )

    coordinates = CoordinateField(
        required=True,
    )
