import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .element import (
    CoordinatesField,
)
from .object_type import (
    LINE_STRING,
)


class PolygonSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [LINE_STRING],
            error='Invalid polygon type'),
    )

    coordinates = CoordinatesField(
        required=True,
    )
