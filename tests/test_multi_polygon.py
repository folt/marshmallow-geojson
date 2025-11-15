"""Tests for MultiPolygonSchema."""

import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import MultiPolygonSchema
from marshmallow_geojson.object_type import MULTI_POLYGON
from tests.test_utils import assert_coordinates_equal


class TestMultiPolygonSchema:
    """Test suite for MultiPolygonSchema validation and serialization."""

    def test_valid_multi_polygon_creation(self, valid_multi_polygon):
        """Test creating a valid MultiPolygon schema."""
        schema = MultiPolygonSchema()
        mp_data = schema.load(valid_multi_polygon)

        assert mp_data["type"] == MULTI_POLYGON
        assert mp_data["type"] == valid_multi_polygon["type"]
        assert len(mp_data["coordinates"]) == len(valid_multi_polygon["coordinates"])

        for poly_idx, polygon in enumerate(mp_data["coordinates"]):
            expected_polygon = valid_multi_polygon["coordinates"][poly_idx]
            assert len(polygon) == len(expected_polygon)

            for ring_idx, ring in enumerate(polygon):
                expected_ring = expected_polygon[ring_idx]
                assert len(ring) == len(expected_ring)

                for coord_idx, coord in enumerate(ring):
                    expected_coord = expected_ring[coord_idx]
                    assert_coordinates_equal(coord, expected_coord)

    def test_multi_polygon_invalid_type(self, invalid_multi_polygon_wrong_type):
        """Test MultiPolygon with invalid type field."""
        schema = MultiPolygonSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_multi_polygon_wrong_type)

        assert "Invalid multi polygon type" in str(exc_info.value)

    def test_multi_polygon_linear_ring_validation(
        self, invalid_multi_polygon_linear_ring_validation
    ):
        """Test MultiPolygon with invalid linear rings."""
        schema = MultiPolygonSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_multi_polygon_linear_ring_validation)

        error_str = str(exc_info.value)
        # Should have errors for both invalid rings
        assert (
            "Linear Ring length must be >=4" in error_str
            or "Linear Rings must start and end at the same coordinate" in error_str
        )

    def test_multi_polygon_serialization(self, valid_multi_polygon):
        """Test MultiPolygon schema serialization to dict."""
        schema = MultiPolygonSchema()
        mp_data = schema.load(valid_multi_polygon)
        serialized = schema.dump(mp_data)

        assert serialized["type"] == "MultiPolygon"
        assert len(serialized["coordinates"]) == len(valid_multi_polygon["coordinates"])

    def test_multi_polygon_json_serialization(self, valid_multi_polygon):
        """Test MultiPolygon schema JSON serialization."""
        schema = MultiPolygonSchema()
        mp_data = schema.load(valid_multi_polygon)
        json_str = schema.dumps(mp_data)

        assert '"type":"MultiPolygon"' in json_str or '"type": "MultiPolygon"' in json_str
        assert str(valid_multi_polygon["coordinates"][0][0][0][0]) in json_str

    def test_multi_polygon_from_json(self, valid_multi_polygon):
        """Test creating MultiPolygon from JSON string."""
        json_str = json.dumps(valid_multi_polygon)
        schema = MultiPolygonSchema()
        mp_data = schema.loads(json_str)

        assert mp_data["type"] == MULTI_POLYGON
        assert len(mp_data["coordinates"]) == len(valid_multi_polygon["coordinates"])

    def test_multi_polygon_with_bbox(self, valid_multi_polygon, bbox_2d):
        """Test MultiPolygon with bounding box."""
        data = {**valid_multi_polygon, "bbox": bbox_2d}
        schema = MultiPolygonSchema()
        mp_data = schema.load(data)

        assert mp_data["bbox"] == bbox_2d
        assert mp_data["type"] == MULTI_POLYGON

    def test_multi_polygon_empty(self):
        """Test MultiPolygon with empty coordinates list."""
        data = {"type": "MultiPolygon", "coordinates": []}
        schema = MultiPolygonSchema()
        mp_data = schema.load(data)

        assert mp_data["type"] == MULTI_POLYGON
        assert len(mp_data["coordinates"]) == 0

    def test_multi_polygon_empty_polygon_rejected(self):
        """Test MultiPolygon with empty Polygon (no rings) is rejected."""
        data = {
            "type": "MultiPolygon",
            "coordinates": [[]],  # Empty Polygon (no rings)
        }
        schema = MultiPolygonSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "at least one linear ring" in error_str or "Polygon must have" in error_str
        assert "RFC 7946" in error_str or "Section 3.1.6" in error_str

    def test_multi_polygon_mixed_valid_invalid_rejected(self):
        """Test MultiPolygon with mix of valid and invalid Polygons is rejected."""
        data = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],  # Valid Polygon (1 ring)
                [],  # Invalid Polygon (no rings)
            ],
        }
        schema = MultiPolygonSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "at least one linear ring" in error_str or "Polygon must have" in error_str

    def test_multi_polygon_minimal_valid(self):
        """Test MultiPolygon with minimal valid Polygons (one ring each)."""
        data = {
            "type": "MultiPolygon",
            "coordinates": [
                [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]],  # Minimal valid Polygon (1 ring)
                [[[2, 2], [3, 2], [3, 3], [2, 3], [2, 2]]],  # Another minimal valid Polygon
            ],
        }
        schema = MultiPolygonSchema()
        mp_data = schema.load(data)
        assert mp_data["type"] == MULTI_POLYGON
        assert len(mp_data["coordinates"]) == 2
        assert len(mp_data["coordinates"][0]) == 1  # One ring
        assert len(mp_data["coordinates"][1]) == 1  # One ring

    def test_multi_polygon_with_holes_valid(self):
        """Test MultiPolygon with Polygons that have holes (multiple rings)."""
        data = {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    [[0, 0], [10, 0], [10, 10], [0, 10], [0, 0]],  # Exterior ring
                    [[2, 2], [8, 2], [8, 8], [2, 8], [2, 2]],  # Interior ring (hole)
                ],
            ],
        }
        schema = MultiPolygonSchema()
        mp_data = schema.load(data)
        assert mp_data["type"] == MULTI_POLYGON
        assert len(mp_data["coordinates"]) == 1
        assert len(mp_data["coordinates"][0]) == 2  # Exterior + 1 hole
