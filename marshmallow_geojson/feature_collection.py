from marshmallow.fields import (
    Nested,
    List,
    Str,
)
from marshmallow.validate import (
    OneOf,
)
from .object_type import (
    FEATURE_COLLECTION,
)
from ._base import BaseSchema
from .feature import FeatureSchema


class FeatureCollectionSchema(BaseSchema):
    type = Str(
        required=True,
        validate=OneOf(
            [FEATURE_COLLECTION],
            error='Invalid feature collection type'
        )
    )

    features = List(
        Nested(FeatureSchema),
        required=True,
    )
