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
    MULTI_POINT,
)


class MultiPointSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_POINT],
            error='Invalid multi point type'),
    )

    coordinates = CoordinateField(
        required=True,
    )
