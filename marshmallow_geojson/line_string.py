from marshmallow.fields import (
    List,
    Tuple,
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    LINE_STRING,
)
from ._base import (
    BaseSchema,
    lon,
    lat,
)


class LineStringSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [LINE_STRING],
            error='Invalid line string type'
        )
    )

    coordinates = List(
        Tuple([lon, lat], required=True),
        required=True,
    )
