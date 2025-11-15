"""MultiPolygon geometry schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import List, Number, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .object_type import MULTI_POLYGON
from .validate import Bbox, LinearRing, NoFeatureMembers, PolygonRings


class MultiPolygonSchema(BaseSchema):
    """Schema for MultiPolygon geometry in GeoJSON format.

    A MultiPolygon is a collection of Polygon geometries. According to RFC 7946
    Section 3.1.7, a MultiPolygon geometry object has coordinates that are an
    array of Polygon coordinate arrays.

    Attributes:
        type: The geometry type, must be "MultiPolygon".
        coordinates: An array of Polygon coordinate arrays, where each Polygon
            is represented by an array of linear rings. Each Polygon must have
            at least one ring (the exterior ring).
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            [MULTI_POLYGON],
            error="Invalid multi polygon type",
        ),
        metadata={
            "title": "Type",
            "description": "The geometry type. Must be 'MultiPolygon'.",
            "example": "MultiPolygon",
        },
    )

    coordinates = List(
        List(
            List(
                List(
                    Number(),
                    required=True,
                ),
                required=True,
                validate=LinearRing(),
            ),
            required=True,
            validate=PolygonRings(),
        ),
        required=True,
        metadata={
            "title": "Coordinates",
            "description": (
                "An array of Polygon coordinate arrays. Each Polygon is "
                "represented by an array of linear rings, with at least one ring (the exterior ring)."
            ),
            "example": [
                [[[125.6, 10.1], [125.7, 10.1], [125.7, 10.2], [125.6, 10.2], [125.6, 10.1]]]
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
        validator = NoFeatureMembers(geometry_type_name="MultiPolygon")
        return self.validate_geometry_data(data, type_validator=validator)
