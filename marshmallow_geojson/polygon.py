from __future__ import annotations

from marshmallow.fields import List, Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .examples import GEOJSON_POLYGON
from .object_type import POLYGON


class PolygonSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [POLYGON],
            error="Invalid polygon type",
        ),
    )

    coordinates = List(
        List(
            Tuple([lon, lat], required=True),
            required=True,
        ),
        required=True,
        metadata=dict(example=GEOJSON_POLYGON["coordinates"]),
    )
