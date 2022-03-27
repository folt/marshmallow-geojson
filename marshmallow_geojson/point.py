from marshmallow.fields import Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .object_type import POINT


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
