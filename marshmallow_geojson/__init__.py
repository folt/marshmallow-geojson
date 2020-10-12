from .point import PointSchema
from .multi_polygon import MultiPolygonSchema
from .line_string import LineStringSchema
from .multi_line_string import MultiLineStringSchema
from .polygon import PolygonSchema
from .multi_point import MultiPointSchema
from .geometry_collection import GeometryCollectionSchema
from .feature import FeatureSchema
from .feature_collection import FeatureCollectionSchema
from .object_type import GeoJSONType
from .geometry import GeometriesSchema
from .geojson import GeoJSONSchema
from .object_type import (
    GeometryType,
    GeoJSONType,
)

__author__ = 'Aliaksandr Vaskevich'
__maintainer__ = __author__

__email__ = 'vaskevic.an@gmail.com'
__license__ = 'MIT'
__version__ = '0.1.18'

__all__ = (
    '__author__',
    '__email__',
    '__license__',
    '__maintainer__',
    '__version__',

    # object type
    'GeometryType',
    'GeoJSONType',

    # schemas
    'PointSchema',
    'MultiPointSchema',
    'LineStringSchema',
    'MultiLineStringSchema',
    'PolygonSchema',
    'MultiPolygonSchema',
    'GeometryCollectionSchema',
    'FeatureSchema',
    'FeatureCollectionSchema',

    'GeometriesSchema',
    'GeoJSONSchema',
)
