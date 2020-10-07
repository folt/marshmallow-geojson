from marshmallow import (
    fields,
    ValidationError
)


class CoordinatesField(fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid coordinate.'
    }

    def __init__(
        self,
        coordinate_type: float = float,
        *args,
        **kwargs,
    ):
        super(CoordinatesField, self).__init__(*args, **kwargs)
        self.coordinate_type = coordinate_type

    def _format_coordinate(self, value):
        lon, lat = value
        return [self.coordinate_type(lon), self.coordinate_type(lat)]

    def _validate_coordinate(self, value):
        if len(value) != 2:
            raise self.make_error('invalid')
        return self._format_coordinate(value)

    def _validated(self, value):
        if value is None:
            return []

        return self._validate_coordinate(value)

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return self._validated(value)


# class CoordinatesField(CoordinateField):
#
#     def _validated(self, value):
#         if value is None:
#             return []
#         return [self._validate_coordinate(item) for item in value]


class GeometryField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value
