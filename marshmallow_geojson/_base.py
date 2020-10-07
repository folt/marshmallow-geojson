import ujson

import marshmallow as ma
from marshmallow.fields import (
    Number,
)
from marshmallow.validate import (
    Range,
)

lon = Number(
    required=True,
    validate=Range(
        min=-180,
        max=180,
        error='Longitude must be between -180, 180'
    )
)

lat = Number(
    required=True,
    validate=Range(
        min=-180,
        max=180,
        error='Latitude must be between -90, 90'
    )
)


class BaseSchema(ma.Schema):

    class Meta:
        render_module = ujson
