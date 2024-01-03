from __future__ import annotations

from marshmallow.fields import List, Str, Tuple
from marshmallow.validate import OneOf

from ._base import BaseSchema, lat, lon
from .examples import GEOJSON_MULTI_POLYGON
from .object_type import MULTI_POLYGON


class MultiPolygonSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_POLYGON],
            error="Invalid multi polygon type",
        ),
    )

    coordinates = List(
        List(
            List(
                Tuple([lon, lat], required=True),
                required=True,
            ),
            required=True,
        ),
        required=True,
        metadata=dict(example=GEOJSON_MULTI_POLYGON["coordinates"]),
    )
