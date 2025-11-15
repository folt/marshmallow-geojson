"""Tests for GeometryCollectionSchema."""

import copy
import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import GeometryCollectionSchema
from marshmallow_geojson.object_type import GEOMETRY_COLLECTION


class TestGeometryCollectionSchema:
    """Test suite for GeometryCollectionSchema validation and serialization."""

    def test_valid_geometry_collection_creation(self, valid_geometry_collection_data):
        """Test creating a valid GeometryCollection schema."""
        schema = GeometryCollectionSchema()
        gc_data = schema.load(valid_geometry_collection_data)

        assert gc_data["type"] == GEOMETRY_COLLECTION
        assert gc_data["type"] == valid_geometry_collection_data["type"]
        assert len(gc_data["geometries"]) == len(valid_geometry_collection_data["geometries"])

        for idx, geometry in enumerate(gc_data["geometries"]):
            expected_geometry = valid_geometry_collection_data["geometries"][idx]
            assert geometry["type"] == expected_geometry["type"]

    def test_geometry_collection_empty(self, valid_geometry_collection_empty):
        """Test GeometryCollection with empty geometries list."""
        schema = GeometryCollectionSchema()
        gc_data = schema.load(valid_geometry_collection_empty)

        assert gc_data["type"] == GEOMETRY_COLLECTION
        assert len(gc_data["geometries"]) == 0

    def test_geometry_collection_nested(self, nested_geometry_collection_data):
        """Test GeometryCollection containing another GeometryCollection.

        Note: While nested geometry collections are not recommended by RFC 7946,
        the library should still validate them correctly.
        """
        schema = GeometryCollectionSchema()
        gc_data = schema.load(nested_geometry_collection_data)

        assert gc_data["type"] == GEOMETRY_COLLECTION
        # Check that nested GeometryCollection is present
        geometry_types = [g["type"] for g in gc_data["geometries"]]
        assert "GeometryCollection" in geometry_types

    def test_geometry_collection_invalid_type(self, geometry_collection_bad_type):
        """Test GeometryCollection with invalid type field."""
        schema = GeometryCollectionSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(geometry_collection_bad_type)

        assert "Invalid geometry collection type" in str(exc_info.value)

    def test_geometry_collection_serialization(self, valid_geometry_collection_data):
        """Test GeometryCollection schema serialization to dict."""
        schema = GeometryCollectionSchema()
        gc_data = schema.load(valid_geometry_collection_data)
        serialized = schema.dump(gc_data)

        assert serialized["type"] == "GeometryCollection"
        assert len(serialized["geometries"]) == len(valid_geometry_collection_data["geometries"])

        # Verify geometries are serialized correctly
        for idx, geometry in enumerate(serialized["geometries"]):
            expected = valid_geometry_collection_data["geometries"][idx]
            assert geometry["type"] == expected["type"]

    def test_geometry_collection_json_serialization(self, valid_geometry_collection_data):
        """Test GeometryCollection schema JSON serialization."""
        schema = GeometryCollectionSchema()
        gc_data = schema.load(valid_geometry_collection_data)
        json_str = schema.dumps(gc_data)

        assert (
            '"type":"GeometryCollection"' in json_str or '"type": "GeometryCollection"' in json_str
        )
        assert '"geometries"' in json_str

    def test_geometry_collection_from_json(self, valid_geometry_collection_data):
        """Test creating GeometryCollection from JSON string."""
        json_str = json.dumps(valid_geometry_collection_data)
        schema = GeometryCollectionSchema()
        gc_data = schema.loads(json_str)

        assert gc_data["type"] == GEOMETRY_COLLECTION
        assert len(gc_data["geometries"]) == len(valid_geometry_collection_data["geometries"])

    def test_geometry_collection_with_bbox(self, valid_geometry_collection_data, bbox_2d):
        """Test GeometryCollection with bounding box."""
        data = copy.deepcopy(valid_geometry_collection_data)
        data["bbox"] = bbox_2d
        schema = GeometryCollectionSchema()
        gc_data = schema.load(data)

        assert gc_data["bbox"] == bbox_2d
        assert gc_data["type"] == GEOMETRY_COLLECTION

    def test_geometry_collection_with_all_geometry_types(self):
        """Test GeometryCollection containing all geometry types."""
        data = {
            "type": "GeometryCollection",
            "geometries": [
                {"type": "Point", "coordinates": [-105.01621, 39.57422]},
                {
                    "type": "MultiPoint",
                    "coordinates": [[-105.01621, 39.57422], [-80.666513, 35.053994]],
                },
                {
                    "type": "LineString",
                    "coordinates": [[-99.113159, 38.869651], [-99.0802, 38.85682]],
                },
                {
                    "type": "MultiLineString",
                    "coordinates": [[[-99.113159, 38.869651], [-99.0802, 38.85682]]],
                },
                {
                    "type": "Polygon",
                    "coordinates": [[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]],
                },
                {
                    "type": "MultiPolygon",
                    "coordinates": [[[[100, 0], [101, 0], [101, 1], [100, 1], [100, 0]]]],
                },
            ],
        }

        schema = GeometryCollectionSchema()
        gc_data = schema.load(data)
        assert gc_data["type"] == GEOMETRY_COLLECTION
        assert len(gc_data["geometries"]) == 6
        assert gc_data["geometries"][0]["type"] == "Point"
        assert gc_data["geometries"][1]["type"] == "MultiPoint"
        assert gc_data["geometries"][2]["type"] == "LineString"
        assert gc_data["geometries"][3]["type"] == "MultiLineString"
        assert gc_data["geometries"][4]["type"] == "Polygon"
        assert gc_data["geometries"][5]["type"] == "MultiPolygon"
