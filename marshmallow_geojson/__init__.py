from .feature import (
    FeatureSchema
)
from .feature_collection import (
    FeatureCollectionSchema
)
from .geometry_collection import (
    GeometryCollectionSchema
)
from .line_string import (
    LineStringSchema
)
from .multi_line_string import (
    MultiLineStringSchema
)
from .multi_point import (
    MultiPointSchema
)
from .multi_polygon import (
    MultiPolygonSchema
)
from .point import (
    PointSchema
)
from .polygon import (
    PolygonSchema
)
from .geojson import (
    GeoJSON,
)
from .object_type import (
    GeometryType,
    GeoJSONType,
)
from .element import (
    CoordinateField,
    CoordinatesField,
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

    # object type
    'GeometryType',
    'GeoJSONType',

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

    # fields
    'CoordinateField',
    'CoordinatesField',

    'GeoJSON',
)
