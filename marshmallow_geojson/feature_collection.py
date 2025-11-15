"""FeatureCollection schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import List, Nested, Number, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .feature import FeatureSchema
from .object_type import FEATURE_COLLECTION
from .validate import Bbox, NoForbiddenMembers


class FeatureCollectionSchema(BaseSchema):
    """Schema for FeatureCollection object in GeoJSON format.

    A FeatureCollection object contains a collection of Feature objects. According
    to RFC 7946 Section 3.3, a FeatureCollection object has a member with the name
    "features". The value of "features" is a JSON array. Each element of the array
    is a Feature object as defined above.

    Attributes:
        type: The object type, must be "FeatureCollection".
        features: An array of Feature objects.
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            choices=[FEATURE_COLLECTION],
            error="Invalid feature collection type",
        ),
        metadata={
            "title": "Type",
            "description": "The object type. Must be 'FeatureCollection'.",
            "example": "FeatureCollection",
        },
    )

    features = List(
        Nested(FeatureSchema()),
        required=True,
        metadata={
            "title": "Features",
            "description": (
                "A JSON array of Feature objects. Each element is a Feature "
                "object as defined in RFC 7946 Section 3.2."
            ),
            "example": [
                {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [125.6, 10.1]},
                    "properties": {"name": "Dinagat Islands"},
                }
            ],
        },
    )

    bbox = List(
        Number(),
        required=False,
        allow_none=True,
        validate=Bbox(),
        metadata={
            "title": "Bounding Box",
            "description": (
                "Coordinate range for a GeoJSON Object. Must be array of length 2*n "
                "where n is the number of dimensions (2, 4, or 6 elements). "
                "For 2D: [west, south, east, north]. "
                "For 3D: [west, south, depth, east, north, height]."
            ),
            "example": [-180.0, -90.0, 180.0, 90.0],
        },
    )

    @pre_load
    def validate_no_forbidden_members(self, data, **kwargs):
        """Validate that FeatureCollection does not contain forbidden members.

        Args:
            data: Input data dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            Validated data dictionary.

        Raises:
            ValidationError: If forbidden members are present.
        """
        validator = NoForbiddenMembers()
        return validator(data)
