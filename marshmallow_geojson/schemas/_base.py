from enum import Enum
import marshmallow as ma


class GeometryType(Enum):
    """
    geometry type
    """
    point = 'Point'
    multi_point = 'MultiPoint'
    line_string = 'LineString'
    multi_line_string = 'MultiLineString'
    polygon = 'Polygon'
    multi_polygon = 'MultiPolygon'
    geometry_collection = 'GeometryCollection'


class GeoJSONType(GeometryType):
    """
    GeoJSON types
    https://www.rfc-editor.org/rfc/rfc7946.html#section-1.4
    """
    feature = 'Feature'
    feature_collection = 'FeatureCollection'


class BaseSchema(ma.Schema):
    pass
