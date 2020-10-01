.. image:: https://travis-ci.org/folt/marshmallow-geojson.svg
   :target: https://travis-ci.org/github/folt/marshmallow-geojson
   :alt: Travis

.. image:: https://codecov.io/gh/folt/marshmallow-geojson/branch/master/graph/badge.svg?token=B5ATYXLBHO
   :target: https://codecov.io/gh/folt/marshmallow-geojson
   :alt: Codecov

marshmallow_geojson 🌍
======================

====================   =======
GeoJSON Objects        Status
====================   =======
Point_                 ✅
MultiPoint_            ❌
LineString_            ❌
MultiLineString_       ❌
Polygon_               ❌
MultiPolygon_          ❌
GeometryCollection_    ❌
Feature_               ❌
FeatureCollection_     ❌
====================   =======

Installation
------------

marshmallow_geojson is compatible with Python 3.7 and 3.8.
The recommended way to install is via poetry_:

.. code::

  poetry add marshmallow_geojson

Using pip to install is also possible.

.. code::

  pip install marshmallow_geojson

GEOJSON
-------
GeoJSON_ is a format for encoding a variety of geographic data structures.

.. code-block::

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

Point
------------------
Simple example data:

.. code-block::

  {
    "type": "Point",
    "coordinates": [
        -105.01621,
        39.57422
    ]
  }


MultiPoint
------------------
Simple example data:

.. code-block::

  {
    "type": "MultiPoint",
    "coordinates": [
        [
            -105.01621,
            39.57422
        ],
        [
            -80.666513,
            35.053994
        ]
    ]
  }


LineString
------------------
Simple example data:

.. code-block::

  {
    "type": "LineString",
    "coordinates": [
        [
            -99.113159,
            38.869651
        ],
        [
            -99.0802,
            38.85682
        ],
        [
            -98.822021,
            38.85682
        ],
        [
            -98.448486,
            38.848264
        ]
    ]
  }


MultiLineString
------------------
Simple example data:

.. code-block::

  {
    "type": "MultiLineString",
    "coordinates": [
        [
              [
                -105.019898,
                39.574997
            ],
            [
                -105.019598,
                39.574898
            ],
            [
                -105.019061,
                39.574782
            ]
        ],
        [
            [
                -105.017173,
                39.574402
            ],
            [
                -105.01698,
                39.574385
            ],
            [
                -105.016636,
                39.574385
            ],
            [
                -105.016508,
                39.574402
            ],
            [
                -105.01595,
                39.57427
            ]
        ],
        [
            [
                -105.014276,
                39.573972
            ],
            [
                -105.014126,
                39.574038
            ],
            [
                -105.013825,
                39.57417
            ],
            [
                -105.01331,
                39.574452
            ]
        ]
    ]
  }


Polygon
------------------
Simple example data:

.. code-block::

  {
    "type": "Polygon",
    "coordinates": [
        [
            [
                100,
                0
            ],
            [
                101,
                0
            ],
            [
                101,
                1
            ],
            [
                100,
                1
            ],
            [
                100,
                0
            ]
        ]
    ]
  }


MultiPolygon
------------------
Simple example data:

.. code-block::

  {
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [
                    107,
                    7
                ],
                [
                    108,
                    7
                ],
                [
                    108,
                    8
                ],
                [
                    107,
                    8
                ],
                [
                    107,
                    7
                ]
            ]
        ],
        [
            [
                [
                    100,
                    0
                ],
                [
                    101,
                    0
                ],
                [
                    101,
                    1
                ],
                [
                    100,
                    1
                ],
                [
                    100,
                    0
                ]
            ]
        ]
    ]
  }


GeometryCollection
------------------
Simple example data:

.. code-block::

  {
    "type": "GeometryCollection",
    "geometries": [
        {
            "type": "Point",
            "coordinates": [
                -80.660805,
                35.049392
            ]
        },
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        -80.664582,
                        35.044965
                    ],
                    [
                        -80.663874,
                        35.04428
                    ],
                    [
                        -80.662586,
                        35.04558
                    ],
                    [
                        -80.663444,
                        35.046036
                    ],
                    [
                        -80.664582,
                        35.044965
                    ]
                ]
            ]
        },
        {
            "type": "LineString",
            "coordinates": [
                [
                    -80.662372,
                    35.059509
                ],
                [
                    -80.662693,
                    35.059263
                ],
                [
                    -80.662844,
                    35.05893
                ]
            ]
        }
    ]
  }


Feature
------------------
Simple example data:

.. code-block::

  {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [
                    -80.724878,
                    35.265454
                ],
                [
                    -80.722646,
                    35.260338
                ],
                [
                    -80.720329,
                    35.260618
                ],
                [
                    -80.71681,
                    35.255361
                ],
                [
                    -80.704793,
                    35.268397
                ],
                [
                    -80.715179,
                    35.267696
                ],
                [
                    -80.721359,
                    35.267276
                ],
                [
                    -80.724878,
                    35.265454
                ]
            ]
        ]
    },
    "properties": {
        "name": "Plaza Road Park"
    }
  }


FeatureCollection
------------------
Simple example data:

.. code-block::

  {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    -80.870885,
                    35.215151
                ]
            },
            "properties": {
                "name": "ABBOTT NEIGHBORHOOD PARK",
                "address": "1300  SPRUCE ST"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -80.724878,
                            35.265454
                        ],
                        [
                            -80.722646,
                            35.260338
                        ],
                        [
                            -80.720329,
                            35.260618
                        ],
                        [
                            -80.704793,
                            35.268397
                        ],

                        [
                            -80.724878,
                            35.265454
                        ]
                    ]
                ]
            },
            "properties": {
                "name": "Plaza Road Park"
            }
        }
    ]
  }

.. _GeoJSON: http://geojson.org/
.. _poetry: https://python-poetry.org/
