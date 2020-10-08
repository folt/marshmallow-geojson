from marshmallow.fields import (
    List,
    Tuple,
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    MULTI_POINT,
)
from ._base import (
    BaseSchema,
    lon,
    lat,
)


class MultiPointSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_POINT],
            error='Invalid multi point type'
        )
    )

    coordinates = List(
        Tuple([lon, lat], required=True),
        required=True
    )

