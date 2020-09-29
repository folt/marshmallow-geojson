from marshmallow import (
    fields,
    ValidationError
)


class CoordinateField(fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid coordinate.'
    }
    coordinate_type = float

    def _format_coordinate(self, value):
        lon = self.coordinate_type(value[0])
        lat = self.coordinate_type(value[1])
        return [lon, lat]

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


class CoordinatesField(CoordinateField):

    def _validated(self, value):
        if value is None:
            return []
        return [self._validate_coordinate(item) for item in value]


class GeometryField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value
