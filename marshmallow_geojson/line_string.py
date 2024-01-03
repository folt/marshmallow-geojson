from __future__ import annotations

from marshmallow.fields import List, Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .examples import GEOJSON_LINE_STRING
from .object_type import LINE_STRING


class LineStringSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [LINE_STRING],
            error="Invalid line string type",
        ),
    )

    coordinates = List(
        Tuple([lon, lat], required=True),
        required=True,
        metadata=dict(example=GEOJSON_LINE_STRING["coordinates"]),
    )
