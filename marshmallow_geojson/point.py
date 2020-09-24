import marshmallow as ma
from .base import BaseSchema
from .element import (
    CoordinateField,
)


class PointSchema(BaseSchema):
    coordinates = CoordinateField(
        required=True,
    )
