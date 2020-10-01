import marshmallow as ma

from marshmallow.validate import (
    OneOf,
)
from marshmallow.fields import (
    Str,
)
from .point import (
    PointSchema
)
from .multi_polygon import (
    MultiPolygonSchema
)
from .line_string import (
    LineStringSchema
)
from .multi_line_string import (
    MultiLineStringSchema
)
from .polygon import (
    PolygonSchema
)
from .multi_point import (
    MultiPointSchema
)
from .geometry_collection import (
    GeometryCollectionSchema
)
from .feature import (
    FeatureSchema
)
from .feature_collection import (
    FeatureCollectionSchema
)
from .object_type import (
    GeoJSONType,
)


class AbstractGeoObject(ma.Schema):
    type_field = 'type'
    object_type_schemas = {
        GeoJSONType.point: PointSchema,
        GeoJSONType.multi_point: MultiPointSchema,
        GeoJSONType.line_string: LineStringSchema,
        GeoJSONType.multi_line_string: MultiLineStringSchema,
        GeoJSONType.polygon: PolygonSchema,
        GeoJSONType.multi_polygon: MultiPolygonSchema,
        GeoJSONType.geometry_collection: GeometryCollectionSchema,
        GeoJSONType.feature: FeatureSchema,
        GeoJSONType.feature_collection: FeatureCollectionSchema,
    }

    def _dump(self, obj, **kwargs):
        if obj is None:
            return None, {'_schema': f'Unknown object class'}
        obj_type = obj.__class__.__name__

        type_schema = self.object_type_schemas.get(obj_type)
        if type_schema is None:
            return None, {'_schema': f'Unsupported object type: {obj_type}'}

        if isinstance(type_schema, ma.Schema):
            schema = type_schema
        else:
            schema = type_schema()

        schema.context.update(getattr(self, "context", {}))
        result = schema.dump(obj, many=False, **kwargs)

        if result is not None:
            result[self.type_field] = obj_type
        return result

    def dump(self, obj, *, many=None, **kwargs):
        result_data = []
        result_errors = {}
        many = self.many if many is None else bool(many)

        if many:
            for index, item in enumerate(obj):
                try:
                    result = self._dump(item, **kwargs)
                    result_data.append(result)
                except ma.ValidationError as error:
                    result_errors[idx] = error.normalized_messages()
                    result_data.append(error.valid_data)
        else:
            result = result_data = self._dump(obj, **kwargs)



        result = result_data
        errors = result_errors

        if not errors:
            return result
        else:
            exc = ma.ValidationError(errors, data=obj, valid_data=result)
            raise exc


class GeoJSON(AbstractGeoObject):
    type = Str(
        required=True,
        validate=OneOf(
            [json_type.value for json_type in GeoJSONType],
            error='Unavailable GeoJSON type'),
    )
