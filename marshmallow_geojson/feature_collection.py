import marshmallow as ma
from marshmallow.fields import (
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .element import (
    GeometryField,
)
from .object_type import (
    FEATURE_COLLECTION,
)


class FeatureCollectionSchema(ma.Schema):
    type = Str(
        required=True,
        validate=OneOf(
            [FEATURE_COLLECTION],
            error='Invalid feature collection type'),
    )
    geometry = GeometryField(
        required=True,
        many=True,
    )
