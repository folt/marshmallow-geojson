import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    FEATURE,
)


class FeatureSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [FEATURE],
            error='Invalid feature type'),
    )
