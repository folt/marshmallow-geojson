import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    MULTI_POLYGON,
)


class MultiPolygonSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_POLYGON],
            error='Invalid multi polygon type'),
    )
