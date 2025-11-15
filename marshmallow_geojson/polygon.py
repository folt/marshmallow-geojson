"""Polygon geometry schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import List, Number, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .object_type import POLYGON
from .validate import Bbox, LinearRing, NoFeatureMembers, PolygonRings


class PolygonSchema(BaseSchema):
    """Schema for Polygon geometry in GeoJSON format.

    A Polygon is a planar surface defined by one exterior boundary and zero or
    more interior boundaries. According to RFC 7946 Section 3.1.6, a Polygon
    geometry object has coordinates that are an array of linear ring coordinate arrays.

    The first element of the coordinates array represents the exterior ring.
    Any subsequent elements represent interior rings (holes).

    Attributes:
        type: The geometry type, must be "Polygon".
        coordinates: An array of linear rings. The first ring is the exterior
            boundary, subsequent rings are interior boundaries (holes).
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            [POLYGON],
            error="Invalid polygon type",
        ),
        metadata={
            "title": "Type",
            "description": "The geometry type. Must be 'Polygon'.",
            "example": "Polygon",
        },
    )

    coordinates = List(
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
        metadata={
            "title": "Coordinates",
            "description": (
                "An array of linear ring coordinate arrays. The first ring "
                "is the exterior boundary, subsequent rings are interior boundaries (holes). "
                "Each linear ring must have at least 4 positions and be closed."
            ),
            "example": [
                [[125.6, 10.1], [125.7, 10.1], [125.7, 10.2], [125.6, 10.2], [125.6, 10.1]]
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
        validator = NoFeatureMembers(geometry_type_name="Polygon")
        return self.validate_geometry_data(data, type_validator=validator)
