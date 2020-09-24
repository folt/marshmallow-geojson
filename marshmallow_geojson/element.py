from marshmallow import (
    fields,
    ValidationError
)


class CoordinatesField(fields.Field):
    default_error_messages = {
        'invalid': 'Not a valid coordinates.'
    }
    coordinates_type = float

    def _format_coordinate(self, value):
        lon = self.coordinates_type(value[0])
        lat = self.coordinates_type(value[1])
        return [lon, lat]

    def _validate_coordinate(self, value):
        if len(value) != 2:
            raise self.make_error('invalid')
        return self._format_coordinate(value)

    def _validated(self, value):
        if value is None:
            return []
        if isinstance(value[0], list):
            return [self._validate_coordinate(item) for item in value]
        else:
            return self._validate_coordinate(value)

    def _serialize(self, value, attr, obj, **kwargs):
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return self._validated(value)
