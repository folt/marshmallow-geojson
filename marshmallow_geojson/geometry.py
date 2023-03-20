from __future__ import annotations

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

    _default_error_messages = {
        'type': 'Invalid input type.',
    }

    def __init__(
        self,
        *,
        only: types.StrSequenceOrSet | None = None,
        exclude: types.StrSequenceOrSet = (),
        many: bool = False,
        context: dict | None = None,
        load_only: types.StrSequenceOrSet = (),
        dump_only: types.StrSequenceOrSet = (),
        partial: bool | types.StrSequenceOrSet = False,
        unknown: str | None = None,
    ):
        super().__init__(
            only=only,
            exclude=exclude,
            many=many,
            context=context,
            load_only=load_only,
            dump_only=dump_only,
            partial=partial,
            unknown=unknown,
        )

        self.object_type_map = {
            GeometryType.point.value: self.point_schema,
            GeometryType.multi_point.value: self.multi_point_schema,
            GeometryType.line_string.value: self.line_string_schema,
            GeometryType.multi_line_string.value: self.multi_line_string_schema,
            GeometryType.polygon.value: self.polygon_schema,
            GeometryType.multi_polygon.value: self.multi_polygon_schema,
        }

    def get_schema(self, object_type: str):
        if object_type in self.object_type_map:
            return self.object_type_map[object_type]
        raise ma.ValidationError(
            {'_schema': f'Unknown object class for {object_type}.'},
        )

    def _list_and_many_or_raise(self, data: typing.Any, many: bool):
        if isinstance(data, list) != many:
            raise ma.ValidationError(
                {'_schema': self._default_error_messages['type']},
            )

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
        many = self.many if many is None else bool(many)
        self._list_and_many_or_raise(data=data, many=many)

        if many:
            result = []
            for item in data:
                schema = self.get_schema(item['type'])
                result.append(
                    schema(
                        only=self.only,
                        exclude=self.exclude,
                        context=self.context,
                        load_only=self.load_only,
                        dump_only=self.dump_only,
                        partial=self.partial,
                        unknown=self.unknown,
                    ).load(
                        data=item,
                        partial=partial,
                        unknown=unknown,
                    )
                )
        else:
            schema = self.get_schema(data['type'])
            result = schema(
                only=self.only,
                exclude=self.exclude,
                context=self.context,
                load_only=self.load_only,
                dump_only=self.dump_only,
                partial=self.partial,
                unknown=self.unknown,
            ).load(
                data=data,
                partial=partial,
                unknown=unknown,
            )

        return result

    def dump(
        self,
        obj: typing.Any,
        *,
        many: bool | None = None,
    ):
        many = self.many if many is None else bool(many)
        self._list_and_many_or_raise(data=obj, many=many)

        if many:
            data = []
            for item in obj:
                schema = self.get_schema(item['type'])
                data.append(
                    schema(
                        only=self.only,
                        exclude=self.exclude,
                        context=self.context,
                        load_only=self.load_only,
                        dump_only=self.dump_only,
                        partial=self.partial,
                        unknown=self.unknown,
                    ).dump(
                        obj=item,
                    )
                )
        else:
            schema = self.get_schema(obj['type'])
            data = schema(
                only=self.only,
                exclude=self.exclude,
                context=self.context,
                load_only=self.load_only,
                dump_only=self.dump_only,
                partial=self.partial,
                unknown=self.unknown,
            ).dump(
                obj=obj,
            )

        return data
