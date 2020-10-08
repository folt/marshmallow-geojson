from marshmallow.fields import (
    List,
    Tuple,
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    MULTI_POLYGON,
)
from ._base import (
    BaseSchema,
    lon,
    lat,
)


class MultiPolygonSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_POLYGON],
            error='Invalid multi polygon type'
        )
    )

    coordinates = List(
        List(
            List(
                Tuple([lon, lat], required=True),
                required=True
            ),
            required=True,
        ),
        required=True,
    )

