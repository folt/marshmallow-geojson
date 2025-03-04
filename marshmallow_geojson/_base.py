from __future__ import annotations

import json

import marshmallow as ma
from marshmallow.fields import Float
from marshmallow.validate import Range

lon = Float(
    required=True,
    validate=Range(min=-180, max=180, error="Longitude must be between -180, 180"),
)

lat = Float(
    required=True,
    validate=Range(min=-90, max=90, error="Latitude must be between -90, 90"),
)


class BaseSchema(ma.Schema):

    class Meta:
        render_module = json
