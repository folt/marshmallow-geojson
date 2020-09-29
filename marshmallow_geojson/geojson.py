import marshmallow as ma

from marshmallow.validate import (
    OneOf,
)
from marshmallow.fields import (
    Str,
)

from .object_type import (
    GeoJSONType,
)


class GeoJSON(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [json_type.value for json_type in GeoJSONType],
            error='Unavailable GeoJSON type'),
    )
