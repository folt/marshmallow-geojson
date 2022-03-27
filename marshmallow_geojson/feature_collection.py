from marshmallow.fields import List, Nested, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .feature import FeatureSchema
from .object_type import FEATURE_COLLECTION


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
