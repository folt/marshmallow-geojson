import marshmallow as ma
from .base import BaseSchema
from .element import (
    CoordinatesField,
)


class PointSchema(BaseSchema):
    coordinates = CoordinatesField(
        required=True,
    )
