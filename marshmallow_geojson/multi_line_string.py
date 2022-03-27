from marshmallow.fields import List, Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .object_type import MULTI_LINE_STRING


class MultiLineStringSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_LINE_STRING],
            error='Invalid multi line string string type'
        )
    )

    coordinates = List(
        List(
            Tuple([lon, lat], required=True),
            required=True
        ),
        required=True,
    )

