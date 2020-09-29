import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    MULTI_LINE_STRING,
)


class MultiLineStringSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_LINE_STRING],
            error='Invalid multi line string type'),
    )
