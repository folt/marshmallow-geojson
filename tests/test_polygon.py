"""Tests for PolygonSchema."""

import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import PolygonSchema
from marshmallow_geojson.object_type import POLYGON
from tests.test_utils import assert_coordinates_equal


class TestPolygonSchema:
    """Test suite for PolygonSchema validation and serialization."""

    def test_valid_polygon_creation(self, valid_polygon_data):
        """Test creating a valid Polygon schema."""
        schema = PolygonSchema()
        p_data = schema.load(valid_polygon_data)

        assert p_data["type"] == POLYGON
        assert p_data["type"] == valid_polygon_data["type"]
        assert len(p_data["coordinates"]) == len(valid_polygon_data["coordinates"])

        for ring_idx, ring in enumerate(p_data["coordinates"]):
            expected_ring = valid_polygon_data["coordinates"][ring_idx]
            assert len(ring) == len(expected_ring)

            for coord_idx, coord in enumerate(ring):
                expected_coord = expected_ring[coord_idx]
                assert_coordinates_equal(coord, expected_coord)

    def test_valid_polygon_with_holes(self, valid_polygon_with_holes):
        """Test Polygon with interior rings (holes)."""
        schema = PolygonSchema()
        p_data = schema.load(valid_polygon_with_holes)

        assert p_data["type"] == POLYGON
        assert len(p_data["coordinates"]) == 2  # exterior + 1 hole

    def test_polygon_linear_ring_must_close(self, invalid_polygon_data_no_loop):
        """Test that Polygon linear rings must start and end at the same coordinate."""
        schema = PolygonSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_polygon_data_no_loop)

        error_str = str(exc_info.value)
        assert "Linear Rings must start and end at the same coordinate" in error_str

    def test_polygon_linear_ring_minimum_length(self, invalid_polygon_data_too_few_points):
        """Test that Polygon linear rings must have at least 4 points."""
        schema = PolygonSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_polygon_data_too_few_points)

        error_str = str(exc_info.value)
        assert "Linear Ring length must be >=4" in error_str
        assert "not 3" in error_str

    def test_polygon_invalid_type(self, invalid_polygon_data_bad_type):
        """Test Polygon with invalid type field."""
        schema = PolygonSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_polygon_data_bad_type)

        assert "Invalid polygon type" in str(exc_info.value)

    def test_polygon_serialization(self, valid_polygon_data):
        """Test Polygon schema serialization to dict."""
        schema = PolygonSchema()
        p_data = schema.load(valid_polygon_data)
        serialized = schema.dump(p_data)

        assert serialized["type"] == "Polygon"
        assert len(serialized["coordinates"]) == len(valid_polygon_data["coordinates"])

        # Verify coordinates structure
        for ring_idx, ring in enumerate(serialized["coordinates"]):
            expected_ring = valid_polygon_data["coordinates"][ring_idx]
            assert len(ring) == len(expected_ring)

    def test_polygon_json_serialization(self, valid_polygon_data):
        """Test Polygon schema JSON serialization."""
        schema = PolygonSchema()
        p_data = schema.load(valid_polygon_data)
        json_str = schema.dumps(p_data)

        assert '"type":"Polygon"' in json_str or '"type": "Polygon"' in json_str
        # Verify coordinates are in JSON
        assert str(valid_polygon_data["coordinates"][0][0][0]) in json_str

    def test_polygon_from_json(self, valid_polygon_data):
        """Test creating Polygon from JSON string."""
        json_str = json.dumps(valid_polygon_data)
        schema = PolygonSchema()
        p_data = schema.loads(json_str)

        assert p_data["type"] == POLYGON
        assert len(p_data["coordinates"]) == len(valid_polygon_data["coordinates"])

    def test_polygon_with_bbox(self, valid_polygon_data, bbox_2d):
        """Test Polygon with bounding box."""
        data = {**valid_polygon_data, "bbox": bbox_2d}
        schema = PolygonSchema()
        p_data = schema.load(data)

        assert p_data["bbox"] == bbox_2d
        assert p_data["type"] == POLYGON

    def test_polygon_exterior_ring_validation(self):
        """Test that exterior ring is properly validated."""
        # Valid polygon with exactly 4 points (minimum)
        data = {
            "type": "Polygon",
            "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 0]]],
        }
        schema = PolygonSchema()
        p_data = schema.load(data)
        assert p_data["type"] == POLYGON
        assert len(p_data["coordinates"][0]) == 4
