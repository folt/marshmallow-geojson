import typing

import marshmallow as ma
from marshmallow import types

from ._base import BaseSchema
from .feature import FeatureSchema
from .feature_collection import FeatureCollectionSchema
from .geometry_collection import GeometryCollectionSchema
from .line_string import LineStringSchema
from .multi_line_string import MultiLineStringSchema
from .multi_point import MultiPointSchema
from .multi_polygon import MultiPolygonSchema
from .object_type import GeoJSONType
from .point import PointSchema
from .polygon import PolygonSchema


class GeoJSONSchema(BaseSchema):
    point_schema = PointSchema
    multi_point_schema = MultiPointSchema
    line_string_schema = LineStringSchema
    multi_line_string_schema = MultiLineStringSchema
    polygon_schema = PolygonSchema
    multi_polygon_schema = MultiPolygonSchema
    geometry_collection_schema = GeometryCollectionSchema
    feature_schema = FeatureSchema
    feature_collection_schema = FeatureCollectionSchema

    def __init__(self, *args, **kwargs):
        super(GeoJSONSchema, self).__init__(*args, **kwargs)
        self.object_type_map = {
            GeoJSONType.point.value: self.point_schema,
            GeoJSONType.multi_point.value: self.multi_point_schema,
            GeoJSONType.line_string.value: self.line_string_schema,
            GeoJSONType.multi_line_string.value: self.multi_line_string_schema,
            GeoJSONType.polygon.value: self.polygon_schema,
            GeoJSONType.multi_polygon.value: self.multi_polygon_schema,
            GeoJSONType.geometry_collection.value: self.geometry_collection_schema,
            GeoJSONType.feature.value: self.feature_schema,
            GeoJSONType.feature_collection.value: self.feature_collection_schema,
        }

    def __validator_geo_json_type(self, geo_type: typing.Any):
        if geo_type not in self.object_type_map:
            raise ma.ValidationError(
                {'_schema': f'Unknown object class for {geo_type}.'})
        return geo_type

    def get_instance_schema(self, data):
        object_type = self.__validator_geo_json_type(data['type'])
        schema = self.object_type_map[object_type]
        return schema()

    def load(
        self,
        data: typing.Union[
            typing.Mapping[str, typing.Any],
            typing.Iterable[typing.Mapping[str, typing.Any]],
        ],
        *,
        many: bool = None,
        partial: typing.Union[bool, types.StrSequenceOrSet] = None,
        unknown: str = None
    ):
        schema = self.get_instance_schema(data)
        return schema.load(data, many=many, partial=partial, unknown=unknown)

    def loads(
        self,
        json_data: str,
        *,
        many: bool = None,
        partial: typing.Union[bool, types.StrSequenceOrSet] = None,
        unknown: str = None,
        **kwargs
    ):
        data = self.opts.render_module.loads(json_data, **kwargs)
        schema = self.get_instance_schema(data)

        return schema.loads(
            json_data, many=many, partial=partial, unknown=unknown
        )
