from __future__ import annotations

from marshmallow.fields import List, Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .examples import GEOJSON_MULTI_LINE_STRING
from .object_type import MULTI_LINE_STRING


class MultiLineStringSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_LINE_STRING],
            error="Invalid multi line string string type",
        ),
    )

    coordinates = List(
        List(Tuple([lon, lat], required=True), required=True),
        required=True,
        metadata=dict(example=GEOJSON_MULTI_LINE_STRING["coordinates"]),
    )
