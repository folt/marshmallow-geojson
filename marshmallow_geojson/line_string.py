from marshmallow.fields import List, Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .object_type import LINE_STRING


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
