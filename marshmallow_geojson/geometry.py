import typing

import marshmallow as ma
from marshmallow import types

from ._base import BaseSchema
from .line_string import LineStringSchema
from .multi_line_string import MultiLineStringSchema
from .multi_point import MultiPointSchema
from .multi_polygon import MultiPolygonSchema
from .object_type import GeometryType
from .point import PointSchema
from .polygon import PolygonSchema


class GeometriesSchema(BaseSchema):
    point_schema = PointSchema
    multi_point_schema = MultiPointSchema
    line_string_schema = LineStringSchema
    multi_line_string_schema = MultiLineStringSchema
    polygon_schema = PolygonSchema
    multi_polygon_schema = MultiPolygonSchema

    def __init__(self, *args, **kwargs):
        super(GeometriesSchema, self).__init__(*args, **kwargs)
        self.object_type_map = {
            GeometryType.point.value: self.point_schema,
            GeometryType.multi_point.value: self.multi_point_schema,
            GeometryType.line_string.value: self.line_string_schema,
            GeometryType.multi_line_string.value: self.multi_line_string_schema,
            GeometryType.polygon.value: self.polygon_schema,
            GeometryType.multi_polygon.value: self.multi_polygon_schema,
        }

    def __validator_geometry_type(self, geo_type: typing.Any):
        if geo_type not in self.object_type_map:
            raise ma.ValidationError(
                {'_schema': f'Unknown object class for {geo_type}.'})
        return geo_type

    def get_instance_schema(self, data):
        object_type = self.__validator_geometry_type(data['type'])
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
