"""Base schema and field definitions for GeoJSON objects."""

from __future__ import annotations

import json
from typing import Any

import marshmallow as ma
from marshmallow import ValidationError
from marshmallow.fields import Number
from marshmallow.validate import Range

lon = Number(
    required=True, validate=Range(min=-180, max=180, error="Longitude must be between -180, 180")
)

lat = Number(
    required=True, validate=Range(min=-90, max=90, error="Latitude must be between -90, 90")
)

alt = Number(
    required=False,
    allow_none=False,
)


def validate_coordinate_values(coords: Any) -> None:
    """Recursively validate coordinate values (longitude and latitude).

    This function validates that all coordinate positions have valid longitude
    and latitude values. It handles coordinates at any nesting level.

    According to RFC 7946 Section 3.1.1, positions MUST have two or more
    elements, and implementations SHOULD NOT extend positions beyond three
    elements.

    Args:
        coords: Coordinate data (can be a single coordinate, list of coordinates,
            or nested lists).

    Raises:
        ValidationError: If any coordinate has invalid longitude, latitude,
            or exceeds the maximum of 3 elements.
    """
    if isinstance(coords, list):
        # Check if this is a coordinate pair/triple (has numeric values)
        if len(coords) >= 2 and all(isinstance(x, (int, float)) for x in coords[:2]):
            # Validate position length (RFC 7946 Section 3.1.1: SHOULD NOT extend beyond 3)
            if len(coords) > 3:
                raise ValidationError(
                    {
                        "coordinates": (
                            "Position must have at most 3 elements (longitude, latitude, optional altitude). "
                            "According to RFC 7946 Section 3.1.1, implementations SHOULD NOT extend "
                            "positions beyond three elements."
                        )
                    }
                )
            # Validate longitude
            if not (-180 <= coords[0] <= 180):
                raise ValidationError({"coordinates": "Longitude must be between -180, 180"})
            # Validate latitude
            if not (-90 <= coords[1] <= 90):
                raise ValidationError({"coordinates": "Latitude must be between -90, 90"})
        else:
            # Recursively validate nested coordinates
            for item in coords:
                validate_coordinate_values(item)


class BaseSchema(ma.Schema):
    """Base schema for all GeoJSON objects.

    All GeoJSON objects must have a "type" field and may optionally include
    a "bbox" (bounding box) field according to RFC 7946 specification.
    """

    class Meta:
        render_module = json
        unknown = "include"

    def validate_geometry_data(
        self,
        data: dict[str, Any],
        type_validator: Any | None = None,
    ) -> dict[str, Any]:
        """Validate coordinate values and check for forbidden members.

        This is a helper method for geometry schemas to validate coordinates
        and check for forbidden members according to RFC 7946 Section 7.1.

        Args:
            data: Input data dictionary.
            type_validator: Optional validator instance to use for checking
                forbidden members (e.g., NoFeatureMembers, NoGeometryMembers).
                If None, only coordinate validation is performed.

        Returns:
            Validated data dictionary.

        Raises:
            ValidationError: If coordinates are invalid or forbidden members present.
        """
        # Validate coordinate values
        if isinstance(data, dict) and "coordinates" in data:
            coords = data["coordinates"]
            validate_coordinate_values(coords)

        # Check for forbidden members (RFC 7946 Section 7.1)
        if type_validator is not None:
            result = type_validator(data)
            if isinstance(result, dict):
                return result

        return data
