"""Validation classes for various types of Geo data."""
from __future__ import annotations

import typing

from marshmallow import ValidationError
from marshmallow.validate import Validator


class Bbox(Validator):
    """ https://datatracker.ietf.org/doc/html/rfc7946#section-5
    A GeoJSON object MAY have a member named "bbox" to include ormation on
    the coordinate range for its Geometries, Features, or FeatureCollections.
    The value of the bbox member MUST be an array of length 2*n where n is
    the number of dimensions represented in the contained geometries, with all
    axes of the most southwesterly point followed by all axes of the more
    northeasterly point.  The axes order of a bbox follows the axes order of
    geometries.
    """

    message_lon = "Longitude must be between -180, 180."
    message_lat = "Latitude must be between -90, 90."
    message_quantity = "The quantity must satisfy 2*n condition."
    default_message = "Wrong geometry in bbox."

    default_min_lon = -180
    default_max_lon = 180
    default_min_lat = -90
    default_max_lat = 90

    def __init__(
        self,
        min_lon=None,
        max_lon=None,
        min_lat=None,
        max_lat=None,
        *,
        error: str | None = None,
    ):
        self.min_lon = self.default_min_lon if min_lon is None else min_lon
        self.max_lon = self.default_max_lon if max_lon is None else max_lon
        self.min_lat = self.default_min_lat if min_lat is None else min_lat
        self.max_lat = self.default_max_lat if max_lat is None else max_lat
        self.error = self.default_message if error is None else error

    def _repr_args(self) -> str:
        return f"min_lon={self.min_lon!r}, " \
               f"max_lon={self.max_lon!r}, " \
               f"min_lat={self.min_lat!r}, " \
               f"max_lat={self.max_lat!r} "

    def _format_error(self, message: str | None) -> str:
        return message or self.error

    def __call__(self, value: typing.List) -> typing.List:
        if len(value) % 2 != 0:
            raise ValidationError(self._format_error(self.message_quantity))

        for index, item in enumerate(value):
            """even elements of Longitude, odd elements of Latitude"""
            if index % 2 == 0:
                if not (self.min_lon < item < self.max_lon):
                    raise ValidationError(self._format_error(self.message_lon))
            else:
                if not (self.min_lat < item < self.max_lat):
                    raise ValidationError(self._format_error(self.message_lat))

        return value
