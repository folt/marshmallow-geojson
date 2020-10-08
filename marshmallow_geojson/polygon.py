from marshmallow.fields import (
    List,
    Tuple,
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    POLYGON,
)
from ._base import (
    BaseSchema,
    lon,
    lat,
)


class PolygonSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [POLYGON],
            error='Invalid polygon type'
        )
    )

    coordinates = List(
        List(
            Tuple([lon, lat], required=True),
            required=True
        ),
        required=True,
    )
