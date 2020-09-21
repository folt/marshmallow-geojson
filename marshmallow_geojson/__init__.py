from .schemas import (
    FeatureSchema,
    FeatureCollectionSchema,
    GeometryCollectionSchema,
    LineStringSchema,
    MultiLineStringSchema,
    MultiPointSchema,
    MultiPolygonSchema,
    PointSchema,
    PolygonSchema,
)
from .geojson import (
    GeoJSON,
)

__author__ = 'Aliaksandr Vaskevich'
__maintainer__ = __author__

__email__ = 'vaskevic.an@gmail.com'
__license__ = 'MIT'
__version__ = '0.1.0'

__all__ = (
    '__author__',
    '__email__',
    '__license__',
    '__maintainer__',
    '__version__',

    # schemas
    'FeatureSchema',
    'FeatureCollectionSchema',

    'GeometryCollectionSchema',
    'LineStringSchema',
    'MultiLineStringSchema',
    'MultiPointSchema',
    'MultiPolygonSchema',
    'PointSchema',
    'PolygonSchema',

    'GeoJSON',
)
