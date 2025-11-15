"""MultiLineString geometry schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import List, Number, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .object_type import MULTI_LINE_STRING
from .validate import Bbox, LineStringCoordinates, NoFeatureMembers


class MultiLineStringSchema(BaseSchema):
    """Schema for MultiLineString geometry in GeoJSON format.

    A MultiLineString is a collection of LineString geometries. According to
    RFC 7946 Section 3.1.5, a MultiLineString geometry object has coordinates
    that are an array of LineString coordinate arrays.

    Attributes:
        type: The geometry type, must be "MultiLineString".
        coordinates: An array of LineString coordinate arrays, where each inner
            array contains two or more positions.
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_LINE_STRING],
            error="Invalid multi line string type",
        ),
        metadata={
            "title": "Type",
            "description": "The geometry type. Must be 'MultiLineString'.",
            "example": "MultiLineString",
        },
    )

    coordinates = List(
        List(
            List(
                Number(),
                required=True,
            ),
            required=True,
            validate=LineStringCoordinates(),
        ),
        required=True,
        metadata={
            "title": "Coordinates",
            "description": (
                "An array of LineString coordinate arrays. Each inner array "
                "must contain at least 2 positions."
            ),
            "example": [[[125.6, 10.1], [125.7, 10.2]], [[125.8, 10.3], [125.9, 10.4]]],
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
        validator = NoFeatureMembers(geometry_type_name="MultiLineString")
        return self.validate_geometry_data(data, type_validator=validator)
