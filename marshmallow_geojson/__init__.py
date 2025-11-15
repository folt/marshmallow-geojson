"""Marshmallow schema validation for GeoJSON.

This package provides Marshmallow schemas for validating and serializing
GeoJSON objects according to RFC 7946 specification.

The main entry point is the :class:`GeoJSONSchema` class, which can handle
all GeoJSON object types: Point, MultiPoint, LineString, MultiLineString,
Polygon, MultiPolygon, GeometryCollection, Feature, and FeatureCollection.

Example:
    Basic usage::

        from marshmallow_geojson import GeoJSONSchema

        schema = GeoJSONSchema()
        data = schema.loads('{"type": "Point", "coordinates": [125.6, 10.1]}')
        # {'type': 'Point', 'coordinates': (125.6, 10.1)}

References:
    https://www.rfc-editor.org/rfc/rfc7946.html
"""

from .feature import FeatureSchema
from .feature_collection import FeatureCollectionSchema
from .geojson import GeoJSONSchema
from .geometry import GeometriesSchema
from .geometry_collection import GeometryCollectionSchema
from .line_string import LineStringSchema
from .multi_line_string import MultiLineStringSchema
from .multi_point import MultiPointSchema
from .multi_polygon import MultiPolygonSchema
from .object_type import GeoJSONType, GeometryType
from .point import PointSchema
from .polygon import PolygonSchema
from .property import PropertiesSchema
from .validate import (
    Bbox,
    LinearRing,
    LineStringCoordinates,
    NoFeatureMembers,
    NoForbiddenMembers,
    NoGeometryMembers,
    PolygonRings,
)

__author__ = "Aliaksandr Vaskevich"
__maintainer__ = __author__

__email__ = "vaskevic.an@gmail.com"
__license__ = "MIT"
__version__ = "0.4.0"

__all__ = (
    "__author__",
    "__email__",
    "__license__",
    "__maintainer__",
    "__version__",
    # object type
    "GeometryType",
    "GeoJSONType",
    # property schemas
    "PropertiesSchema",
    # schemas
    "PointSchema",
    "MultiPointSchema",
    "LineStringSchema",
    "MultiLineStringSchema",
    "PolygonSchema",
    "MultiPolygonSchema",
    "GeometryCollectionSchema",
    "FeatureSchema",
    "FeatureCollectionSchema",
    "GeometriesSchema",
    "GeoJSONSchema",
    # validators
    "Bbox",
    "LinearRing",
    "LineStringCoordinates",
    "NoFeatureMembers",
    "NoForbiddenMembers",
    "NoGeometryMembers",
    "PolygonRings",
)
