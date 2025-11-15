"""MultiPoint geometry schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import List, Number, Str
from marshmallow.validate import Length, OneOf

from ._base import BaseSchema
from .object_type import MULTI_POINT
from .validate import Bbox, NoFeatureMembers


class MultiPointSchema(BaseSchema):
    """Schema for MultiPoint geometry in GeoJSON format.

    A MultiPoint is a collection of Point geometries. According to RFC 7946
    Section 3.1.3, a MultiPoint geometry object has coordinates that are an
    array of positions.

    Attributes:
        type: The geometry type, must be "MultiPoint".
        coordinates: An array of coordinate positions, each representing a point.
            Each position is [longitude, latitude] or [longitude, latitude, altitude].
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_POINT],
            error="Invalid multi point type",
        ),
        metadata={
            "title": "Type",
            "description": "The geometry type. Must be 'MultiPoint'.",
            "example": "MultiPoint",
        },
    )

    coordinates = List(
        List(
            Number(),
            required=True,
            validate=Length(min=2, max=3, error="Coordinates must have 2 or 3 elements"),
        ),
        required=True,
        metadata={
            "title": "Coordinates",
            "description": (
                "An array of positions. Each position is "
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
        validator = NoFeatureMembers(geometry_type_name="MultiPoint")
        return self.validate_geometry_data(data, type_validator=validator)
