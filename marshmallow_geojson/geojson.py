from __future__ import annotations

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
    """Schema for validating and serializing GeoJSON objects.

    This schema can handle all GeoJSON object types: Point, MultiPoint,
    LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection,
    Feature, and FeatureCollection. It automatically selects the appropriate
    schema based on the "type" field in the input data.

    Attributes:
        point_schema: Schema class for Point geometry.
        multi_point_schema: Schema class for MultiPoint geometry.
        line_string_schema: Schema class for LineString geometry.
        multi_line_string_schema: Schema class for MultiLineString geometry.
        polygon_schema: Schema class for Polygon geometry.
        multi_polygon_schema: Schema class for MultiPolygon geometry.
        geometry_collection_schema: Schema class for GeometryCollection.
        feature_schema: Schema class for Feature objects.
        feature_collection_schema: Schema class for FeatureCollection objects.
    """

    point_schema = PointSchema
    multi_point_schema = MultiPointSchema
    line_string_schema = LineStringSchema
    multi_line_string_schema = MultiLineStringSchema
    polygon_schema = PolygonSchema
    multi_polygon_schema = MultiPolygonSchema
    geometry_collection_schema = GeometryCollectionSchema
    feature_schema = FeatureSchema
    feature_collection_schema = FeatureCollectionSchema

    _default_error_messages = {
        "type": "Invalid input type.",
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
        """Initialize GeoJSONSchema.

        Args:
            only: Fields to include during serialization/deserialization.
            exclude: Fields to exclude during serialization/deserialization.
            many: Whether to handle multiple objects (list) or single object.
            context: Optional context dictionary for custom validation.
            load_only: Fields that are only used during deserialization.
            dump_only: Fields that are only used during serialization.
            partial: Whether to allow partial data. Can be True/False or a
                sequence of field names.
            unknown: How to handle unknown fields. Can be 'raise', 'exclude',
                or 'include'.
        """
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

    def get_schema(self, object_type: str):
        """Get the appropriate schema class for a given GeoJSON object type.

        Args:
            object_type: The GeoJSON object type string (e.g., "Point", "Feature").

        Returns:
            The schema class for the given object type.

        Raises:
            ValidationError: If the object type is not recognized.
        """
        if object_type in self.object_type_map:
            return self.object_type_map[object_type]
        raise ma.ValidationError(
            {"_schema": f"Unknown object class for {object_type}."},
        )

    def _list_and_many_or_raise(self, data: typing.Any, many: bool):
        """Validate that data type matches the many parameter.

        Args:
            data: Input data to validate.
            many: Whether data should be a list (True) or a single object (False).

        Raises:
            ValidationError: If data type doesn't match the many parameter.
        """
        if isinstance(data, list) != many:
            raise ma.ValidationError(
                {"_schema": self._default_error_messages["type"]},
            )

    def load(
        self,
        data: typing.Mapping[str, typing.Any] | typing.Iterable[typing.Mapping[str, typing.Any]],
        *,
        many: bool | None = None,
        partial: bool | types.StrSequenceOrSet | None = None,
        unknown: str | None = None,
    ):
        """Deserialize and validate GeoJSON data.

        Args:
            data: GeoJSON object(s) to deserialize. Can be a single object or
                a list of objects.
            many: Whether to deserialize multiple objects. If None, uses the
                schema's default.
            partial: Whether to allow partial data. Can be True/False or a
                sequence of field names.
            unknown: How to handle unknown fields. Can be 'raise', 'exclude', or
                'include'.

        Returns:
            Deserialized and validated GeoJSON data.

        Raises:
            ValidationError: If validation fails.
        """
        many = self.many if many is None else bool(many)
        self._list_and_many_or_raise(data=data, many=many)

        if many:
            result = []
            for item in typing.cast(typing.Iterable[typing.Mapping[str, typing.Any]], data):
                schema = self.get_schema(item["type"])
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
            schema = self.get_schema(typing.cast(typing.Mapping[str, typing.Any], data)["type"])
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
        """Serialize GeoJSON object(s) to Python dict(s).

        Args:
            obj: GeoJSON object(s) to serialize. Can be a single object or
                a list of objects.
            many: Whether to serialize multiple objects. If None, uses the
                schema's default.

        Returns:
            Serialized GeoJSON data as Python dict(s).

        Raises:
            ValidationError: If serialization fails.
        """
        many = self.many if many is None else bool(many)
        self._list_and_many_or_raise(data=obj, many=many)

        if many:
            data = []
            for item in obj:
                schema = self.get_schema(item["type"])
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
            schema = self.get_schema(obj["type"])
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
