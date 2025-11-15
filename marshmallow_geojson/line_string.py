"""LineString geometry schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import List, Number, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .object_type import LINE_STRING
from .validate import Bbox, LineStringCoordinates, NoFeatureMembers


class LineStringSchema(BaseSchema):
    """Schema for LineString geometry in GeoJSON format.

    A LineString is a curve with linear interpolation between points. According to
    RFC 7946 Section 3.1.4, a LineString geometry object has coordinates that
    are an array of two or more positions.

    Attributes:
        type: The geometry type, must be "LineString".
        coordinates: An array of two or more coordinate positions that form a line.
            Each position is [longitude, latitude] or [longitude, latitude, altitude].
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            [LINE_STRING],
            error="Invalid line string type",
        ),
        metadata={
            "title": "Type",
            "description": "The geometry type. Must be 'LineString'.",
            "example": "LineString",
        },
    )

    coordinates = List(
        List(
            Number(),
            required=True,
        ),
        required=True,
        validate=LineStringCoordinates(),
        metadata={
            "title": "Coordinates",
            "description": (
                "An array of two or more positions. Each position is "
                "[longitude, latitude] or [longitude, latitude, altitude]."
            ),
            "example": [[125.6, 10.1], [125.7, 10.2]],
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
        validator = NoFeatureMembers(geometry_type_name="LineString")
        return self.validate_geometry_data(data, type_validator=validator)
