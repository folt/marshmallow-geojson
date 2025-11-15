"""GeoJSON object type definitions.

This module defines the valid GeoJSON object types as specified in
RFC 7946 Section 1.4.

References:
    https://www.rfc-editor.org/rfc/rfc7946.html#section-1.4
"""

from __future__ import annotations

from enum import Enum

POINT = "Point"
MULTI_POINT = "MultiPoint"
LINE_STRING = "LineString"
MULTI_LINE_STRING = "MultiLineString"
POLYGON = "Polygon"
MULTI_POLYGON = "MultiPolygon"
GEOMETRY_COLLECTION = "GeometryCollection"


class GeometryType(Enum):
    """Enumeration of GeoJSON geometry types.

    According to RFC 7946 Section 1.4, the term "geometry type" refers to
    seven case-sensitive strings: "Point", "MultiPoint", "LineString",
    "MultiLineString", "Polygon", "MultiPolygon", and "GeometryCollection".

    References:
        https://www.rfc-editor.org/rfc/rfc7946.html#section-1.4
    """

    point = POINT
    multi_point = MULTI_POINT
    line_string = LINE_STRING
    multi_line_string = MULTI_LINE_STRING
    polygon = POLYGON
    multi_polygon = MULTI_POLYGON
    geometry_collection = GEOMETRY_COLLECTION


FEATURE = "Feature"
FEATURE_COLLECTION = "FeatureCollection"


class GeoJSONType(Enum):
    """Enumeration of all GeoJSON object types.

    According to RFC 7946 Section 1.4, the term "GeoJSON types" refers to
    nine case-sensitive strings: "Feature", "FeatureCollection", and the
    seven geometry types (Point, MultiPoint, LineString, MultiLineString,
    Polygon, MultiPolygon, and GeometryCollection).

    References:
        https://www.rfc-editor.org/rfc/rfc7946.html#section-1.4
    """

    point = POINT
    multi_point = MULTI_POINT
    line_string = LINE_STRING
    multi_line_string = MULTI_LINE_STRING
    polygon = POLYGON
    multi_polygon = MULTI_POLYGON
    geometry_collection = GEOMETRY_COLLECTION
    feature = FEATURE
    feature_collection = FEATURE_COLLECTION
