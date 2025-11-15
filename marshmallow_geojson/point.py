"""Point geometry schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import List, Number, Str
from marshmallow.validate import Length, OneOf

from ._base import BaseSchema
from .object_type import POINT
from .validate import Bbox, NoFeatureMembers


class PointSchema(BaseSchema):
    """Schema for Point geometry in GeoJSON format.

    A Point is a single position specified by its coordinates. According to
    RFC 7946 Section 3.1.2, a Point geometry object has coordinates that are
    a single position [longitude, latitude] or [longitude, latitude, altitude].

    Attributes:
        type: The geometry type, must be "Point".
        coordinates: A single coordinate position [lon, lat] or [lon, lat, alt].
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            [POINT],
            error="Invalid point type",
        ),
        metadata={
            "title": "Type",
            "description": "The geometry type. Must be 'Point'.",
            "example": "Point",
        },
    )

    coordinates = List(
        Number(),
        required=True,
        validate=Length(min=2, max=3, error="Coordinates must have 2 or 3 elements"),
        metadata={
            "title": "Coordinates",
            "description": (
                "A single coordinate position. Must be [longitude, latitude] "
                "or [longitude, latitude, altitude]."
            ),
            "example": [125.6, 10.1],
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
    def validate_coordinates(self, data, **kwargs):
        """Validate coordinate values and check for forbidden members.

        Args:
            data: Input data dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            Validated data dictionary.

        Raises:
            ValidationError: If coordinates are invalid or forbidden members present.
        """
        validator = NoFeatureMembers(geometry_type_name="Point")
        return self.validate_geometry_data(data, type_validator=validator)
