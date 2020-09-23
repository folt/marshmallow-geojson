import marshmallow as ma
from marshmallow.validate import (
    OneOf,
)
from marshmallow.fields import (
    Str,
)
from .object_type import (
    GeometryType
)


class BaseSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [json_type.value for json_type in GeometryType],
            error='Unavailable GeoJSON type'),
    )
