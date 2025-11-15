[![GitHub Actions status for master branch](https://github.com/folt/marshmallow-geojson/actions/workflows/main.yml/badge.svg)](https://github.com/folt/marshmallow-geojson/actions?query=workflow%3A%22Python+package%22)
[![Latest PyPI package version](https://badge.fury.io/py/marshmallow-geojson.svg)](https://pypi.org/project/marshmallow-geojson/)
[![Codecov](https://codecov.io/gh/folt/marshmallow-geojson/branch/master/graph/badge.svg?token=B5ATYXLBHO)](https://codecov.io/gh/folt/marshmallow-geojson)
[![Downloads](https://pepy.tech/badge/marshmallow-geojson)](https://pepy.tech/project/marshmallow-geojson)

# marshmallow-geojson 🌍

A schema-based, Marshmallow library for validating and working with [GeoJSON](http://geojson.org/) data according to [RFC 7946](https://tools.ietf.org/html/rfc7946) specification.

## Supported GeoJSON Objects

| GeoJSON Objects        | Status | Description                          |
|------------------------|--------|--------------------------------------|
| Point                  | ✅      | A single geographic coordinate       |
| MultiPoint             | ✅      | Multiple points                       |
| LineString             | ✅      | A sequence of connected points forming a line |
| MultiLineString        | ✅      | Multiple line strings                 |
| Polygon                | ✅      | A closed area, optionally with holes |
| MultiPolygon           | ✅      | Multiple polygons                     |
| GeometryCollection     | ✅      | Collection of different geometry types |
| Feature                | ✅      | Geometry with properties              |
| FeatureCollection      | ✅      | Collection of features               |
| Bbox                   | ✅      | Bounding box validation               |

## Installation

marshmallow-geojson is compatible with Python 3.9 and up.

The recommended way to install is via [poetry](https://python-poetry.org/):

```shell
poetry add marshmallow_geojson
```

Using pip to install is also possible:

```shell
pip install marshmallow-geojson
```

## Quick Start

```python
from marshmallow_geojson import GeoJSONSchema

# Create a schema instance
schema = GeoJSONSchema()

# Load GeoJSON from JSON string
geojson_text = '{"type": "Point", "coordinates": [-105.01621, 39.57422]}'
data = schema.loads(geojson_text)
print(data)
# {'type': 'Point', 'coordinates': [-105.01621, 39.57422]}

# Load GeoJSON from dictionary
geojson_dict = {"type": "Point", "coordinates": [-105.01621, 39.57422]}
data = schema.load(geojson_dict)
print(data)
# {'type': 'Point', 'coordinates': [-105.01621, 39.57422]}

# Dump GeoJSON to JSON string
json_str = schema.dumps(geojson_dict)
print(json_str)
# '{"type": "Point", "coordinates": [-105.01621, 39.57422]}'
```

## GeoJSON Types with Visualizations

<table style="width: 100%;">
<thead>
<tr>
<th style="width: 20%;">Type</th>
<th style="width: 20%; text-align: center;">Visualization</th>
<th style="width: 60%;">Usage</th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>Point</strong><br>A single geographic coordinate</td>
<td style="text-align: center;"><img src="https://raw.githubusercontent.com/folt/marshmallow-geojson/master/assets/point.jpg" alt="Point" width="150"></td>
<td>

```python
from marshmallow_geojson import GeoJSONSchema

data = {
    "type": "Point",
    "coordinates": [-105.01621, 39.57422]
}
schema = GeoJSONSchema()
point = schema.load(data)

# Or with altitude
data_3d = {
    "type": "Point",
    "coordinates": [-105.01621, 39.57422, 100.5]
}
point_3d = schema.load(data_3d)

# From JSON string
json_str = '{"type": "Point", "coordinates": [-105.01621, 39.57422]}'
point = schema.loads(json_str)
```

</td>
</tr>
<tr>
<td><strong>MultiPoint</strong><br>Multiple points</td>
<td style="text-align: center;"><img src="https://raw.githubusercontent.com/folt/marshmallow-geojson/master/assets/multi_point.jpg" alt="MultiPoint" width="150"></td>
<td>

```python
from marshmallow_geojson import GeoJSONSchema

data = {
    "type": "MultiPoint",
    "coordinates": [
        [-105.01621, 39.57422],
        [-80.666513, 35.053994]
    ]
}
schema = GeoJSONSchema()
multi_point = schema.load(data)

# Dump to JSON
json_output = schema.dumps(multi_point)
```

</td>
</tr>
<tr>
<td><strong>LineString</strong><br>A sequence of connected points forming a line</td>
<td style="text-align: center;"><img src="https://raw.githubusercontent.com/folt/marshmallow-geojson/master/assets/line_string.jpg" alt="LineString" width="150"></td>
<td>

```python
from marshmallow_geojson import GeoJSONSchema

data = {
    "type": "LineString",
    "coordinates": [
        [-99.113159, 38.869651],
        [-99.0802, 38.85682],
        [-98.822021, 38.85682],
        [-98.448486, 38.848264]
    ]
}
schema = GeoJSONSchema()
line_string = schema.load(data)

# Minimal LineString (2 points)
minimal = {
    "type": "LineString",
    "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]]
}
line = schema.load(minimal)
```

</td>
</tr>
<tr>
<td><strong>MultiLineString</strong><br>Multiple line strings</td>
<td style="text-align: center;"><img src="https://raw.githubusercontent.com/folt/marshmallow-geojson/master/assets/multi_line_string.jpg" alt="MultiLineString" width="150"></td>
<td>

```python
from marshmallow_geojson import GeoJSONSchema

data = {
    "type": "MultiLineString",
    "coordinates": [
        [[-105.019898, 39.574997],
         [-105.019598, 39.574898],
         [-105.019061, 39.574782]],
        [[-105.017173, 39.574402],
         [-105.01698, 39.574385],
         [-105.016636, 39.574385]]
    ]
}
schema = GeoJSONSchema()
multi_line_string = schema.load(data)

# With bbox
data_with_bbox = {
    "type": "MultiLineString",
    "bbox": [-180.0, -90.0, 180.0, 90.0],
    "coordinates": [[[-105.019898, 39.574997], [-105.019598, 39.574898]]]
}
result = schema.load(data_with_bbox)
```

</td>
</tr>
<tr>
<td><strong>Polygon</strong><br>A closed area, optionally with holes</td>
<td style="text-align: center;"><img src="https://raw.githubusercontent.com/folt/marshmallow-geojson/master/assets/polygon.jpg" alt="Polygon" width="150"></td>
<td>

```python
from marshmallow_geojson import GeoJSONSchema

# Simple polygon
data = {
    "type": "Polygon",
    "coordinates": [
        [[100, 0],
         [101, 0],
         [101, 1],
         [100, 1],
         [100, 0]]
    ]
}
schema = GeoJSONSchema()
polygon = schema.load(data)

# Polygon with holes (interior rings)
data_with_holes = {
    "type": "Polygon",
    "coordinates": [
        [[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]],  # Exterior
        [[100.2, 0.2], [100.8, 0.2], [100.8, 0.8], [100.2, 0.8], [100.2, 0.2]]  # Hole
    ]
}
polygon_with_holes = schema.load(data_with_holes)
```

</td>
</tr>
<tr>
<td><strong>MultiPolygon</strong><br>Multiple polygons</td>
<td style="text-align: center;"><img src="https://raw.githubusercontent.com/folt/marshmallow-geojson/master/assets/multi_polygon.jpg" alt="MultiPolygon" width="150"></td>
<td>

```python
from marshmallow_geojson import GeoJSONSchema

data = {
    "type": "MultiPolygon",
    "coordinates": [
        [[[107, 7], [108, 7],
          [108, 8], [107, 8],
          [107, 7]]],
        [[[100, 0], [101, 0],
          [101, 1], [100, 1],
          [100, 0]]]
    ]
}
schema = GeoJSONSchema()
multi_polygon = schema.load(data)

# Serialize back to dict
serialized = schema.dump(multi_polygon)
```

</td>
</tr>
<tr>
<td><strong>GeometryCollection</strong><br>Collection of different geometry types</td>
<td style="text-align: center;"><img src="https://raw.githubusercontent.com/folt/marshmallow-geojson/master/assets/geometry_collection.jpg" alt="GeometryCollection" width="150"></td>
<td>

```python
from marshmallow_geojson import GeoJSONSchema

data = {
    "type": "GeometryCollection",
    "geometries": [
        {
            "type": "Point",
            "coordinates": [-80.660805, 35.049392]
        },
        {
            "type": "Polygon",
            "coordinates": [[[-80.664582, 35.044965],
                             [-80.663874, 35.04428],
                             [-80.662586, 35.04558],
                             [-80.663444, 35.046036],
                             [-80.664582, 35.044965]]]
        },
        {
            "type": "LineString",
            "coordinates": [[-80.662372, 35.059509],
                            [-80.662693, 35.059263],
                            [-80.662844, 35.05893]]
        }
    ]
}
schema = GeoJSONSchema()
geometry_collection = schema.load(data)

# Empty GeometryCollection
empty = {
    "type": "GeometryCollection",
    "geometries": []
}
empty_collection = schema.load(empty)
```

</td>
</tr>
</tbody>
</table>

## Features and FeatureCollections

### Feature

A geometry with properties.

```python
from marshmallow_geojson import GeoJSONSchema

# Basic Feature
data = {
    "type": "Feature",
    "properties": {
        "name": "Dinagat Islands",
        "population": 10000
    },
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-80.724878, 35.265454],
                [-80.722646, 35.260338],
                [-80.720329, 35.260618],
                [-80.71681, 35.255361],
                [-80.704793, 35.268397],
                [-80.724878, 35.265454]
            ]
        ]
    }
}
schema = GeoJSONSchema()
feature = schema.load(data)

# Feature with Point geometry
point_feature = {
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [-74.006, 40.7128]
    },
    "properties": {
        "name": "New York",
        "population": 8336817
    }
}
feature = schema.load(point_feature)

# Feature with null geometry (unlocated feature)
null_geometry_feature = {
    "type": "Feature",
    "geometry": None,
    "properties": {
        "name": "Unknown Location"
    }
}
feature = schema.load(null_geometry_feature)

# Feature with ID
feature_with_id = {
    "type": "Feature",
    "id": "feature-123",
    "geometry": {
        "type": "Point",
        "coordinates": [-105.01621, 39.57422]
    },
    "properties": {
        "name": "Test Feature"
    }
}
feature = schema.load(feature_with_id)

# Feature with bbox
feature_with_bbox = {
    "type": "Feature",
    "bbox": [-180.0, -90.0, 180.0, 90.0],
    "geometry": {
        "type": "Point",
        "coordinates": [-105.01621, 39.57422]
    },
    "properties": {}
}
feature = schema.load(feature_with_bbox)
```

### FeatureCollection

A collection of features.

```python
from marshmallow_geojson import GeoJSONSchema

# Basic FeatureCollection
data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-80.870885, 35.215151]
            },
            "properties": {
                "name": "Location 1"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-80.724878, 35.265454],
                        [-80.722646, 35.260338],
                        [-80.720329, 35.260618],
                        [-80.704793, 35.268397],
                        [-80.724878, 35.265454]
                    ]
                ]
            },
            "properties": {
                "name": "Location 2"
            }
        }
    ]
}
schema = GeoJSONSchema()
feature_collection = schema.load(data)

# Empty FeatureCollection
empty_fc = {
    "type": "FeatureCollection",
    "features": []
}
empty_collection = schema.load(empty_fc)

# FeatureCollection with mixed geometry types
mixed_fc = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-105.01621, 39.57422]},
            "properties": {"type": "point"}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]]
            },
            "properties": {"type": "line"}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]
            },
            "properties": {"type": "polygon"}
        }
    ]
}
mixed_collection = schema.load(mixed_fc)

# FeatureCollection with bbox
fc_with_bbox = {
    "type": "FeatureCollection",
    "bbox": [-180.0, -90.0, 180.0, 90.0],
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [-105.01621, 39.57422]},
            "properties": {}
        }
    ]
}
collection = schema.load(fc_with_bbox)

# Serialize FeatureCollection to JSON
json_output = schema.dumps(feature_collection)
```

## Universal GeoJSONSchema

marshmallow-geojson provides a universal `GeoJSONSchema` that automatically handles all GeoJSON object types. This is a unique feature not available in other GeoJSON libraries.

```python
from marshmallow_geojson import GeoJSONSchema

schema = GeoJSONSchema()

# Automatically handles Point
point_data = {"type": "Point", "coordinates": [-105.01621, 39.57422]}
point = schema.load(point_data)

# Automatically handles Feature
feature_data = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-105.01621, 39.57422]},
    "properties": {"name": "Test"}
}
feature = schema.load(feature_data)

# Automatically handles FeatureCollection
fc_data = {
    "type": "FeatureCollection",
    "features": [feature_data]
}
feature_collection = schema.load(fc_data)

# Works with mixed types in many=True mode
schema_many = GeoJSONSchema(many=True)
mixed_data = [point_data, feature_data, fc_data]
results = schema_many.load(mixed_data)

# Load from JSON string - automatically detects type
json_point = '{"type": "Point", "coordinates": [-105.01621, 39.57422]}'
point = schema.loads(json_point)

json_feature = '{"type": "Feature", "geometry": {"type": "Point", "coordinates": [-105.01621, 39.57422]}, "properties": {}}'
feature = schema.loads(json_feature)

# Get specific schema for a type
point_schema_class = schema.get_schema("Point")
feature_schema_class = schema.get_schema("Feature")

# Handle multiple objects with many=True
json_array = '[{"type": "Point", "coordinates": [-105.01621, 39.57422]}, {"type": "LineString", "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]]}]'
schema_many = GeoJSONSchema(many=True)
results = schema_many.loads(json_array)
# Returns list of validated objects
```

## GeometriesSchema

For working with geometry objects only (excluding Feature and FeatureCollection), use `GeometriesSchema`:

```python
from marshmallow_geojson import GeometriesSchema

schema = GeometriesSchema()

# Works with all geometry types
point_data = {"type": "Point", "coordinates": [-105.01621, 39.57422]}
point = schema.load(point_data)

polygon_data = {"type": "Polygon", "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]}
polygon = schema.load(polygon_data)

# Rejects Feature and FeatureCollection
# schema.load({"type": "Feature", ...})  # Raises ValidationError
```

## Custom Properties Schemas

You can define typed properties schemas for type-safe feature properties:

```python
from marshmallow.fields import Str, Int, Nested
from marshmallow_geojson import GeoJSONSchema, PropertiesSchema, FeatureSchema

class CityPropertiesSchema(PropertiesSchema):
    name = Str(required=True)
    population = Int(required=True)
    country = Str(required=True)

class CityFeatureSchema(FeatureSchema):
    properties = Nested(
        CityPropertiesSchema,
        required=True,
    )

class CityGeoJSONSchema(GeoJSONSchema):
    feature_schema = CityFeatureSchema

# Usage
schema = CityGeoJSONSchema()
data = {
    "type": "Feature",
    "properties": {
        "name": "New York",
        "population": 8336817,
        "country": "USA"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [-74.006, 40.7128]
    }
}
city = schema.load(data)
print(city['properties']['name'])  # "New York"
print(city['properties']['population'])  # 8336817
```

## Marshmallow-Specific Features

marshmallow-geojson supports all standard Marshmallow schema features:

### Field Filtering (only/exclude)

```python
from marshmallow_geojson import GeoJSONSchema

# Include only specific fields
schema = GeoJSONSchema(only=('type', 'geometry'))
data = schema.load(feature_data)
# Only 'type' and 'geometry' fields are included

# Exclude specific fields
schema = GeoJSONSchema(exclude=('properties',))
data = schema.load(feature_data)
# 'properties' field is excluded
```

### Partial Loading

```python
from marshmallow_geojson import GeoJSONSchema

schema = GeoJSONSchema(partial=True)
# Allows partial data loading
partial_data = {
    "type": "Feature",
    "geometry": {"type": "Point", "coordinates": [-105.01621, 39.57422]}
}
result = schema.load(partial_data, partial=('properties',))
```

### Unknown Field Handling

```python
from marshmallow_geojson import GeoJSONSchema

# Exclude unknown fields
schema = GeoJSONSchema(unknown='exclude')
data_with_extra = {
    "type": "Point",
    "coordinates": [-105.01621, 39.57422],
    "extra_field": "extra_value"
}
result = schema.load(data_with_extra)
# 'extra_field' is automatically excluded

# Raise error on unknown fields
schema = GeoJSONSchema(unknown='raise')
# schema.load(data_with_extra)  # Raises ValidationError
```

### Many Mode

Handle multiple GeoJSON objects at once:

```python
from marshmallow_geojson import GeoJSONSchema

schema = GeoJSONSchema(many=True)

# Load multiple objects
data_list = [
    {"type": "Point", "coordinates": [-105.01621, 39.57422]},
    {"type": "LineString", "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]]},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-80.870885, 35.215151]}, "properties": {}}
]
results = schema.load(data_list)

# Works with JSON strings too
json_str = '[{"type": "Point", "coordinates": [-105.01621, 39.57422]}]'
results = schema.loads(json_str)
```

## Validation

marshmallow-geojson automatically validates:

- **Coordinate ranges**: Longitude must be between -180 and 180, latitude between -90 and 90
- **Geometry types**: Ensures correct type strings according to RFC 7946
- **Structure**: Validates GeoJSON object structure and required fields
- **Linear Rings**: Polygon rings must have at least 4 positions and be closed
- **LineString**: Must have at least 2 positions
- **Bounding Box**: Validates bbox structure (2, 4, or 6 elements) and coordinate order
- **Type mixing**: Prevents forbidden members according to RFC 7946 Section 7.1

### Example: Invalid Coordinates

```python
from marshmallow_geojson import GeoJSONSchema
from marshmallow.exceptions import ValidationError

schema = GeoJSONSchema()
try:
    data = {"type": "Point", "coordinates": [200, 50]}  # Invalid longitude (> 180)
    schema.load(data)
except ValidationError as e:
    print(e.messages)
    # {'coordinates': ['Longitude must be between -180, 180']}
```

### Example: Invalid Polygon

```python
from marshmallow_geojson import GeoJSONSchema
from marshmallow.exceptions import ValidationError

schema = GeoJSONSchema()
try:
    # Polygon ring must have at least 4 positions and be closed
    data = {
        "type": "Polygon",
        "coordinates": [[[100, 0], [101, 0], [100, 0]]]  # Only 3 positions, not closed
    }
    schema.load(data)
except ValidationError as e:
    print(e.messages)
    # {'coordinates': ['Linear Ring must have at least 4 positions']}
```

## Bounding Box Validation

marshmallow-geojson includes comprehensive bounding box validation:

```python
from marshmallow.fields import List, Number
from marshmallow_geojson import PointSchema
from marshmallow_geojson.validate import Bbox

class PointWithBboxSchema(PointSchema):
    bbox = List(
        Number(),
        required=False,
        allow_none=True,
        validate=Bbox()
    )

schema = PointWithBboxSchema()

# Valid 2D bbox
data = {
    "type": "Point",
    "coordinates": [-105.01621, 39.57422],
    "bbox": [-180.0, -90.0, 180.0, 90.0]
}
result = schema.load(data)

# Valid 3D bbox
data = {
    "type": "Point",
    "coordinates": [-105.01621, 39.57422],
    "bbox": [-180.0, -90.0, -100.0, 180.0, 90.0, 100.0]
}
result = schema.load(data)
```

## Flask Integration

marshmallow-geojson works seamlessly with Flask for building GeoJSON APIs:

```python
from flask import Flask, request, jsonify
from marshmallow_geojson import GeoJSONSchema
from marshmallow.exceptions import ValidationError

app = Flask(__name__)
schema = GeoJSONSchema()

@app.route('/geojson', methods=['POST'])
def create_geojson():
    try:
        data = schema.loads(request.data)
        # Your business logic here
        return jsonify(schema.dump(data)), 201
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400

@app.route('/geojson/many', methods=['POST'])
def create_geojson_many():
    schema_many = GeoJSONSchema(many=True)
    try:
        data = schema_many.loads(request.data)
        return jsonify(schema_many.dump(data)), 201
    except ValidationError as e:
        return jsonify({'errors': e.messages}), 400
```

## Compatibility with Other Libraries

marshmallow-geojson is designed to work well with popular Python libraries:

### Marshmallow

Built on Marshmallow, so you get all the benefits:

- Schema-based validation
- JSON serialization/deserialization
- Field filtering and partial loading
- Custom validators
- Integration with Flask, FastAPI, and other frameworks

### GeoPandas

You can convert between marshmallow-geojson and GeoPandas:

```python
import geopandas as gpd
from marshmallow_geojson import GeoJSONSchema

# Convert FeatureCollection to GeoDataFrame
schema = GeoJSONSchema()
feature_collection = schema.load(fc_data)
geojson_dict = schema.dump(feature_collection)
gdf = gpd.GeoDataFrame.from_features(geojson_dict["features"])

# Convert GeoDataFrame to FeatureCollection
features = gdf.to_dict("records")
fc_data = {"type": "FeatureCollection", "features": features}
feature_collection = schema.load(fc_data)
```

### Shapely

Convert to/from Shapely geometries:

```python
from shapely.geometry import Point as ShapelyPoint
from marshmallow_geojson import GeoJSONSchema

schema = GeoJSONSchema()

# Marshmallow GeoJSON to Shapely
point_data = {"type": "Point", "coordinates": [-105.01621, 39.57422]}
point = schema.load(point_data)
shapely_point = ShapelyPoint(point['coordinates'][0], point['coordinates'][1])

# Shapely to Marshmallow GeoJSON
shapely_geom = ShapelyPoint(-105.01621, 39.57422)
point_data = {
    "type": "Point",
    "coordinates": [shapely_geom.x, shapely_geom.y]
}
point = schema.load(point_data)
```

## Testing

Run the test suite:

```shell
poetry run pytest
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](https://github.com/folt/marshmallow-geojson/blob/master/CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/folt/marshmallow-geojson/blob/master/LICENSE) file for details.

## Links

- [GitHub Repository](https://github.com/folt/marshmallow-geojson)
- [PyPI Package](https://pypi.org/project/marshmallow-geojson/)
- [GeoJSON Specification](http://geojson.org/)
- [RFC 7946](https://tools.ietf.org/html/rfc7946)
- [Marshmallow Documentation](https://marshmallow.readthedocs.io/)
