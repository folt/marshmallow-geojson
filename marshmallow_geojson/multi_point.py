from marshmallow.fields import List, Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .object_type import MULTI_POINT


class MultiPointSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_POINT],
            error='Invalid multi point type'
        )
    )

    coordinates = List(
        Tuple([lon, lat], required=True),
        required=True
    )

