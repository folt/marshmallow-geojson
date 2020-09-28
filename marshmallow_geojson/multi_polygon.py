import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .element import (
    CoordinatesField,
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

    coordinates = CoordinatesField(
        required=True,
        many=True,
    )
