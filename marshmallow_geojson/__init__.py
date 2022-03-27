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

    # property schemas
    'PropertiesSchema',

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
