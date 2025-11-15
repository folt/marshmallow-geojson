"""Validation classes for various types of Geo data."""

from __future__ import annotations

from marshmallow import ValidationError
from marshmallow.validate import Validator


class Bbox(Validator):
    """Validate bounding box according to RFC 7946 Section 5.

    A bounding box must be an array of length 2*n where n is the number of
    dimensions. For 2D: [west, south, east, north]. For 3D: [west, south, depth,
    east, north, height]. For 1D: [min, max] (2 elements).

    The validator checks:
    - Length must be 2, 4, or 6 elements
    - Longitude values must be in [-180, 180] (inclusive)
    - Latitude values must be in [-90, 90] (inclusive)
    - For 2D: south <= north
    - For 3D: depth <= height
    - Antimeridian crossing (west > east) is allowed with span < 360 degrees

    Args:
        min_lon: Minimum longitude (default: -180)
        max_lon: Maximum longitude (default: 180)
        min_lat: Minimum latitude (default: -90)
        max_lat: Maximum latitude (default: 90)
        error: Custom error message

    References:
        https://datatracker.ietf.org/doc/html/rfc7946#section-5
    """

    message_lon = "Longitude must be between -180, 180."
    message_lat = "Latitude must be between -90, 90."
    message_quantity = (
        "Bounding box must have 2, 4, or 6 elements (got {length}). "
        "According to RFC 7946, bbox length must be 2*n where n is the number of dimensions."
    )
    message_lat_order = (
        "Bounding box north latitude ({north}) must be >= south latitude ({south}). "
        "According to RFC 7946 Section 5.3, even pole cases follow this rule."
    )
    message_depth_order = "Bounding box depth ({depth}) must be <= height ({height})"
    message_antimeridian = (
        "Bounding box with antimeridian crossing: west ({west}) > east ({east}) "
        "but span is >= 360 degrees, which is invalid."
    )
    default_message = "Wrong geometry in bbox."

    default_min_lon = -180
    default_max_lon = 180
    default_min_lat = -90
    default_max_lat = 90

    def __init__(
        self,
        min_lon=None,
        max_lon=None,
        min_lat=None,
        max_lat=None,
        *,
        error: str | None = None,
    ):
        """Initialize Bbox validator.

        Args:
            min_lon: Minimum longitude (default: -180)
            max_lon: Maximum longitude (default: 180)
            min_lat: Minimum latitude (default: -90)
            max_lat: Maximum latitude (default: 90)
            error: Custom error message
        """
        self.min_lon = self.default_min_lon if min_lon is None else min_lon
        self.max_lon = self.default_max_lon if max_lon is None else max_lon
        self.min_lat = self.default_min_lat if min_lat is None else min_lat
        self.max_lat = self.default_max_lat if max_lat is None else max_lat
        self.error: str = self.default_message if error is None else error

    def _repr_args(self) -> str:
        """Return string representation of validator arguments.

        Returns:
            String representation of validator configuration parameters.
        """
        return (
            f"min_lon={self.min_lon!r}, "
            f"max_lon={self.max_lon!r}, "
            f"min_lat={self.min_lat!r}, "
            f"max_lat={self.max_lat!r}"
        )

    def _format_error(self, message: str | None) -> str:
        """Format error message.

        Args:
            message: Optional custom error message. If None, uses the default
                error message.

        Returns:
            Formatted error message string.
        """
        return message or self.error

    def _validate_2d_bbox(self, bbox: list[float]) -> None:
        """Validate 2D bounding box [west, south, east, north].

        Args:
            bbox: Bounding box array with 4 elements.

        Raises:
            ValidationError: If bbox doesn't meet RFC 7946 requirements.
        """
        west, south, east, north = bbox

        # Validate longitude range (inclusive boundaries)
        if not (self.min_lon <= west <= self.max_lon):
            raise ValidationError(f"Bounding box west longitude must be in [-180, 180], got {west}")
        if not (self.min_lon <= east <= self.max_lon):
            raise ValidationError(f"Bounding box east longitude must be in [-180, 180], got {east}")

        # Validate latitude range (inclusive boundaries)
        if not (self.min_lat <= south <= self.max_lat):
            raise ValidationError(f"Bounding box south latitude must be in [-90, 90], got {south}")
        if not (self.min_lat <= north <= self.max_lat):
            raise ValidationError(f"Bounding box north latitude must be in [-90, 90], got {north}")

        # Validate latitude order (south <= north)
        if north < south:
            raise ValidationError(self.message_lat_order.format(north=north, south=south))

        # Validate longitude order (antimeridian crossing allowed)
        if west > east:
            # Antimeridian crossing: check that it's reasonable
            # The span should be less than 360 degrees
            span = (180 - west) + (east - (-180))
            if span >= 360:
                raise ValidationError(self.message_antimeridian.format(west=west, east=east))

    def _validate_3d_bbox(self, bbox: list[float]) -> None:
        """Validate 3D bounding box [west, south, depth, east, north, height].

        Args:
            bbox: Bounding box array with 6 elements.

        Raises:
            ValidationError: If bbox doesn't meet RFC 7946 requirements.
        """
        west, south, depth, east, north, height = bbox

        # Validate longitude range (inclusive boundaries)
        if not (self.min_lon <= west <= self.max_lon):
            raise ValidationError(f"Bounding box west longitude must be in [-180, 180], got {west}")
        if not (self.min_lon <= east <= self.max_lon):
            raise ValidationError(f"Bounding box east longitude must be in [-180, 180], got {east}")

        # Validate latitude range (inclusive boundaries)
        if not (self.min_lat <= south <= self.max_lat):
            raise ValidationError(f"Bounding box south latitude must be in [-90, 90], got {south}")
        if not (self.min_lat <= north <= self.max_lat):
            raise ValidationError(f"Bounding box north latitude must be in [-90, 90], got {north}")

        # Validate latitude order (south <= north)
        if north < south:
            raise ValidationError(self.message_lat_order.format(north=north, south=south))

        # Validate longitude order (antimeridian crossing allowed)
        if west > east:
            span = (180 - west) + (east - (-180))
            if span >= 360:
                raise ValidationError(self.message_antimeridian.format(west=west, east=east))

        # Validate depth/height order (depth <= height)
        if depth > height:
            raise ValidationError(self.message_depth_order.format(depth=depth, height=height))

    def __call__(self, value: list) -> list:
        """Validate bounding box value.

        Args:
            value: Bounding box array.

        Returns:
            The validated bbox (same list).

        Raises:
            ValidationError: If bbox doesn't meet RFC 7946 requirements.
        """
        if value is None:
            return value

        length = len(value)
        if length not in (2, 4, 6):
            raise ValidationError(self.message_quantity.format(length=length))

        # Validate 2D bbox: [west, south, east, north]
        if length == 4:
            self._validate_2d_bbox(value)

        # Validate 3D bbox: [west, south, depth, east, north, height]
        elif length == 6:
            self._validate_3d_bbox(value)

        # For 1D bbox (length == 2), we don't have specific validation rules
        # in RFC 7946 but we can validate that values are numeric
        elif length == 2:
            if not all(isinstance(x, (int, float)) for x in value):
                raise ValidationError("Bounding box must contain only numeric values")

        return value


class LinearRing(Validator):
    """Validate that a linear ring meets GeoJSON requirements.

    A linear ring is a closed LineString with four or more positions. The first
    and last positions must be equivalent (they must contain identical values).

    According to RFC 7946 Section 3.1.6, a linear ring must have at least 4
    positions and be closed.

    References:
        https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.6
    """

    message_min_length = "Linear Ring length must be >=4, not {length}"
    message_not_closed = (
        "Linear Rings must start and end at the same coordinate. Start {start}, End {end}."
    )

    def __call__(self, value: list) -> list:
        """Validate linear ring.

        Args:
            value: List of coordinates representing the linear ring.

        Returns:
            The validated linear ring (same list).

        Raises:
            ValidationError: If the linear ring has fewer than 4 coordinates
                or if the first and last coordinates are not equal.
        """
        if (length := len(value)) < 4:
            raise ValidationError(self.message_min_length.format(length=length))

        start = value[0]
        end = value[-1]

        if start != end:
            raise ValidationError(self.message_not_closed.format(start=start, end=end))

        return value


class LineStringCoordinates(Validator):
    """Validate that a LineString has at least 2 coordinates.

    According to RFC 7946 Section 3.1.4, a LineString must have two or more
    positions.

    References:
        https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.4
    """

    message_min_length = (
        "LineString must have at least 2 coordinates (got {length}). "
        "According to RFC 7946 Section 3.1.4, LineString coordinates must be "
        "an array of two or more positions."
    )

    def __call__(self, value: list) -> list:
        """Validate LineString coordinates.

        Args:
            value: List of coordinates representing a LineString.

        Returns:
            The validated coordinates list.

        Raises:
            ValidationError: If the LineString has fewer than 2 coordinates.
        """
        if len(value) < 2:
            raise ValidationError(self.message_min_length.format(length=len(value)))
        return value


class PolygonRings(Validator):
    """Validate that a Polygon has at least one linear ring.

    According to RFC 7946 Section 3.1.6, a Polygon must have an array of linear
    ring coordinate arrays. The first ring is the exterior ring, and any others
    are interior rings. A Polygon must have at least one ring (the exterior ring).

    References:
        https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.6
    """

    message_min_rings = (
        "Polygon must have at least one linear ring (the exterior ring). "
        "According to RFC 7946 Section 3.1.6, Polygon coordinates must be "
        "an array of linear ring coordinate arrays."
    )

    def __call__(self, value: list) -> list:
        """Validate Polygon rings.

        Args:
            value: List of linear rings representing a Polygon.

        Returns:
            The validated rings list.

        Raises:
            ValidationError: If the Polygon has no rings.
        """
        if len(value) == 0:
            raise ValidationError(self.message_min_rings)
        return value


class NoFeatureMembers(Validator):
    """Validate that Geometry objects do not contain Feature-defining members.

    According to RFC 7946 Section 7.1, Geometry objects MUST NOT contain
    "geometry" or "properties" members (which define Feature objects).
    Geometry objects also MUST NOT contain "features" member (which defines
    FeatureCollection objects).

    This validator should be used with @pre_load or @pre_dump decorator on
    Geometry schema classes.

    References:
        https://datatracker.ietf.org/doc/html/rfc7946#section-7.1
    """

    forbidden_fields = {"geometry", "properties", "features"}

    def __init__(self, geometry_type_name: str = "Geometry"):
        """Initialize NoFeatureMembers validator.

        Args:
            geometry_type_name: Name of the geometry type (for error messages).
        """
        self.geometry_type_name = geometry_type_name

    def __call__(self, value: dict) -> dict:
        """Validate that no forbidden members are present.

        Args:
            value: Input data dictionary.

        Returns:
            The input data if valid.

        Raises:
            ValidationError: If forbidden members are present.
        """
        if isinstance(value, dict):
            for field in self.forbidden_fields:
                if field in value:
                    obj_type = (
                        "Feature" if field in ("geometry", "properties") else "FeatureCollection"
                    )
                    raise ValidationError(
                        f"{self.geometry_type_name} objects MUST NOT contain "
                        f'"{field}" member. According to RFC 7946 Section 7.1, '
                        f'"{field}" defines {obj_type} objects.'
                    )
        return value


class NoGeometryMembers(Validator):
    """Validate that Feature objects do not contain Geometry-defining members.

    According to RFC 7946 Section 7.1, Feature objects MUST NOT contain
    "coordinates" or "geometries" members (which define Geometry objects).
    Feature objects also MUST NOT contain "features" member (which defines
    FeatureCollection objects).

    This validator should be used with @pre_load or @pre_dump decorator on
    Feature schema classes.

    References:
        https://datatracker.ietf.org/doc/html/rfc7946#section-7.1
    """

    forbidden_fields = {"coordinates", "geometries", "features"}

    def __call__(self, value: dict) -> dict:
        """Validate that no forbidden members are present.

        Args:
            value: Input data dictionary.

        Returns:
            The input data if valid.

        Raises:
            ValidationError: If forbidden members are present.
        """
        if isinstance(value, dict):
            for field in self.forbidden_fields:
                if field in value:
                    obj_type = (
                        "Geometry"
                        if field in ("coordinates", "geometries")
                        else "FeatureCollection"
                    )
                    raise ValidationError(
                        f'Feature objects MUST NOT contain "{field}" member. '
                        f'According to RFC 7946 Section 7.1, "{field}" defines '
                        f"{obj_type} objects."
                    )
        return value


class NoForbiddenMembers(Validator):
    """Validate that FeatureCollection objects do not contain forbidden members.

    According to RFC 7946 Section 7.1:
    - FeatureCollection MUST NOT contain "coordinates" or "geometries"
      (Geometry-defining)
    - FeatureCollection MUST NOT contain "geometry" or "properties"
      (Feature-defining)

    This validator should be used with @pre_load or @pre_dump decorator on
    FeatureCollection schema classes.

    References:
        https://datatracker.ietf.org/doc/html/rfc7946#section-7.1
    """

    forbidden_fields = {"coordinates", "geometries", "geometry", "properties"}

    def __call__(self, value: dict) -> dict:
        """Validate that no forbidden members are present.

        Args:
            value: Input data dictionary.

        Returns:
            The input data if valid.

        Raises:
            ValidationError: If forbidden members are present.
        """
        if isinstance(value, dict):
            for field in self.forbidden_fields:
                if field in value:
                    obj_type = "Geometry" if field in ("coordinates", "geometries") else "Feature"
                    raise ValidationError(
                        f'FeatureCollection objects MUST NOT contain "{field}" '
                        f'member. According to RFC 7946 Section 7.1, "{field}" '
                        f"defines {obj_type} objects."
                    )
        return value
