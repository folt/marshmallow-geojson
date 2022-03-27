from marshmallow.fields import List, Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .object_type import POLYGON


class PolygonSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [POLYGON],
            error='Invalid polygon type'
        )
    )

    coordinates = List(
        List(
            Tuple([lon, lat], required=True),
            required=True
        ),
        required=True,
    )
