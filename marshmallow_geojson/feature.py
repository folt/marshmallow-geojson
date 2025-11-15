"""Feature schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import Dict, List, Nested, Number, Raw, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .geometry import GeometriesSchema
from .object_type import FEATURE
from .validate import Bbox, NoGeometryMembers


class FeatureSchema(BaseSchema):
    """Schema for Feature object in GeoJSON format.

    A Feature object represents a spatially bounded thing. According to RFC 7946
    Section 3.2, a Feature object has a "geometry" property and a "properties"
    property. The value of the geometry property is a geometry object as defined
    above or a JSON null value. The value of the properties property is a JSON
    object or a JSON null value.

    A Feature object may have a member named "id". If present, the value of the
    id member is either a JSON string or number.

    Attributes:
        type: The object type, must be "Feature".
        geometry: A geometry object as defined above or a JSON null value.
            According to RFC 7946 Section 3.2, this member is required but
            may be null for unlocated features.
        properties: A JSON object or JSON null value containing feature properties.
            According to RFC 7946 Section 3.2, this member is required.
        id: Optional feature identifier. Can be a string or integer, or None.
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            [FEATURE],
            error="Invalid feature type",
        ),
        metadata={
            "title": "Type",
            "description": "The object type. Must be 'Feature'.",
            "example": "Feature",
        },
    )

    geometry = Nested(
        GeometriesSchema(),
        required=True,
        allow_none=True,
        metadata={
            "title": "Geometry",
            "description": (
                "A geometry object as defined above or a JSON null value. "
                "According to RFC 7946 Section 3.2, this member is required but "
                "may be null for unlocated features."
            ),
            "example": {"type": "Point", "coordinates": [125.6, 10.1]},
        },
    )

    properties = Dict(
        required=True,
        allow_none=True,
        metadata={
            "title": "Properties",
            "description": (
                "A JSON object or JSON null value containing feature properties. "
                "According to RFC 7946 Section 3.2, this member is required."
            ),
            "example": {"name": "Dinagat Islands"},
        },
    )

    id = Raw(
        required=False,
        allow_none=True,
        metadata={
            "title": "ID",
            "description": (
                "A unique identifier for the feature. If present, must be a JSON string or number."
            ),
            "example": "feature-1",
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
    def validate_no_geometry_members(self, data, **kwargs):
        """Validate that Feature does not contain Geometry-defining members.

        Args:
            data: Input data dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            Validated data dictionary.

        Raises:
            ValidationError: If forbidden members are present.
        """
        validator = NoGeometryMembers()
        return validator(data)
