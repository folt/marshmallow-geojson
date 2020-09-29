.. image:: https://travis-ci.org/folt/marshmallow-geojson.svg
   :target: https://travis-ci.org/github/folt/marshmallow-geojson
   :alt: Travis

.. image:: https://codecov.io/gh/folt/marshmallow-geojson/branch/master/graph/badge.svg?token=B5ATYXLBHO
   :target: https://codecov.io/gh/folt/marshmallow-geojson
   :alt: Codecov

marshmallow_geojson 🌍
======================

===================   =======
GeoJSON Objects       Status
===================   =======
Point                 ✅
MultiPoint            ❌
LineString            ❌
MultiLineString       ❌
Polygon               ✅
MultiPolygon          ❌
GeometryCollection    ❌
Feature               ❌
FeatureCollection     ❌
===================   =======

GEOJSON
-------
_GeoJSON is a format for encoding a variety of geographic data structures.
.. example-code::

  {
    "type": "Feature",
    "geometry": {
      "type": "Point",
      "coordinates": [125.6, 10.1]
    },
    "properties": {
      "name": "Dinagat Islands"
    }
  }

GeoJSON supports the following geometry types: Point, LineString, Polygon,
MultiPoint, MultiLineString, and MultiPolygon. Geometric objects with
additional properties are Feature objects. Sets of features are contained by
FeatureCollection objects.

.. _GeoJSON: http://geojson.org/
