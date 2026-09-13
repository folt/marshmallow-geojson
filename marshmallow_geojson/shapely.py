"""Optional Shapely interoperability helpers for GeoJSON data."""

from __future__ import annotations

import importlib
import json
from typing import Any

__all__ = [
    "from_shapely",
    "geojson_to_shapely",
    "shapely_to_geojson",
    "to_shapely",
]


def _shapely() -> Any:
    """Import Shapely lazily so it remains an optional dependency."""
    try:
        return importlib.import_module("shapely")
    except ImportError as exc:
        raise ImportError("Shapely is required for this functionality.") from exc


def geojson_to_shapely(geojson: Any) -> Any:
    """Convert GeoJSON data to a Shapely geometry object."""
    if geojson is None:
        return None

    if isinstance(geojson, (str, bytes, bytearray)):
        geojson = json.loads(geojson)

    if hasattr(geojson, "__geo_interface__"):
        return geojson

    if isinstance(geojson, dict):
        geo_type = geojson.get("type")

        if geo_type == "Feature":
            return geojson_to_shapely(geojson.get("geometry"))

        if geo_type == "FeatureCollection":
            geometries: list[Any] = []
            for feature in geojson.get("features", []):
                if not isinstance(feature, dict):
                    continue
                geometry = geojson_to_shapely(feature.get("geometry"))
                if geometry is not None:
                    geometries.append(geometry)
            shapely = _shapely()
            if len(geometries) == 1:
                return geometries[0]
            return shapely.GeometryCollection(geometries)

        if geo_type == "Null":
            return None

        if "coordinates" in geojson or "geometries" in geojson:
            return _shapely().shape(geojson)

    if isinstance(geojson, list):
        geometries = [geojson_to_shapely(item) for item in geojson]
        shapely = _shapely()
        if len(geometries) == 1:
            return geometries[0]
        return shapely.GeometryCollection(geometries)

    return geojson


def shapely_to_geojson(geometry: Any) -> Any:
    """Convert a Shapely geometry object to a GeoJSON dictionary."""
    if geometry is None:
        return None

    if isinstance(geometry, (str, bytes, bytearray)):
        return json.loads(geometry)

    if hasattr(geometry, "__geo_interface__"):
        return dict(geometry.__geo_interface__)

    if isinstance(geometry, dict):
        return geometry

    if isinstance(geometry, list):
        return [shapely_to_geojson(item) for item in geometry]

    return geometry


def to_shapely(geojson: Any) -> Any:
    """Convert GeoJSON data to a Shapely geometry object."""
    return geojson_to_shapely(geojson)


def from_shapely(geometry: Any) -> Any:
    """Convert a Shapely geometry object to a GeoJSON dictionary."""
    return shapely_to_geojson(geometry)
