from marshmallow import (
    fields,
    ValidationError
)


class CoordinateField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return value

    def _deserialize(self, value, attr, data, **kwargs):
        return value
