import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)

from .object_type import (
    LINE_STRING,
)


class LineStringSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [LINE_STRING],
            error='Invalid line string type'),
    )
