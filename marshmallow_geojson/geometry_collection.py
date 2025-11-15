"""GeometryCollection schema for GeoJSON."""

from __future__ import annotations

from marshmallow import pre_load
from marshmallow.fields import List, Nested, Number, Str
from marshmallow.validate import OneOf

from ._base import BaseSchema
from .object_type import GEOMETRY_COLLECTION
from .validate import Bbox, NoFeatureMembers


class GeometryCollectionSchema(BaseSchema):
    """Schema for GeometryCollection in GeoJSON format.

    A GeometryCollection is a collection of geometry objects of any type. According
    to RFC 7946 Section 3.1.8, a GeometryCollection has a "geometries" property
    containing an array of geometry objects.

    A GeometryCollection may contain other GeometryCollection objects, allowing
    for nested collections.

    Attributes:
        type: The geometry type, must be "GeometryCollection".
        geometries: An array of geometry objects. Each geometry can be any valid
            GeoJSON geometry type, including another GeometryCollection.
        bbox: Optional bounding box array.
    """

    type = Str(
        required=True,
        validate=OneOf(
            [GEOMETRY_COLLECTION],
            error="Invalid geometry collection type",
        ),
        metadata={
            "title": "Type",
            "description": "The geometry type. Must be 'GeometryCollection'.",
            "example": "GeometryCollection",
        },
    )

    geometries = List(
        Nested("GeometriesSchema"),
        required=True,
        metadata={
            "title": "Geometries",
            "description": (
                "An array of geometry objects. Each geometry can be any valid "
                "GeoJSON geometry type, including another GeometryCollection."
            ),
            "example": [
                {"type": "Point", "coordinates": [125.6, 10.1]},
                {"type": "LineString", "coordinates": [[125.6, 10.1], [125.7, 10.2]]},
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
    def validate_no_feature_members(self, data, **kwargs):
        """Validate that GeometryCollection does not contain Feature-defining members.

        Args:
            data: Input data dictionary.
            **kwargs: Additional keyword arguments.

        Returns:
            Validated data dictionary.

        Raises:
            ValidationError: If forbidden members are present.
        """
        validator = NoFeatureMembers(geometry_type_name="GeometryCollection")
        return validator(data)
