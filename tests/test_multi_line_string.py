"""Tests for MultiLineStringSchema."""

import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import MultiLineStringSchema
from marshmallow_geojson.object_type import MULTI_LINE_STRING
from tests.test_utils import assert_coordinates_equal


class TestMultiLineStringSchema:
    """Test suite for MultiLineStringSchema validation and serialization."""

    def test_valid_multi_line_string_creation(self, valid_multi_line_string_data):
        """Test creating a valid MultiLineString schema."""
        schema = MultiLineStringSchema()
        mls_data = schema.load(valid_multi_line_string_data)

        assert mls_data["type"] == MULTI_LINE_STRING
        assert mls_data["type"] == valid_multi_line_string_data["type"]
        assert len(mls_data["coordinates"]) == len(valid_multi_line_string_data["coordinates"])

        for line_idx, line in enumerate(mls_data["coordinates"]):
            expected_line = valid_multi_line_string_data["coordinates"][line_idx]
            assert len(line) == len(expected_line)

            for coord_idx, coord in enumerate(line):
                expected_coord = expected_line[coord_idx]
                assert_coordinates_equal(coord, expected_coord)

    def test_multi_line_string_invalid_type(self, invalid_multi_line_string_bad_type):
        """Test MultiLineString with invalid type field."""
        schema = MultiLineStringSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_multi_line_string_bad_type)

        assert "Invalid multi line string type" in str(exc_info.value)

    def test_multi_line_string_empty(self, invalid_multi_line_string_empty):
        """Test MultiLineString with empty coordinates list."""
        schema = MultiLineStringSchema()
        mls_data = schema.load(invalid_multi_line_string_empty)

        assert mls_data["type"] == MULTI_LINE_STRING
        assert len(mls_data["coordinates"]) == 0

    def test_multi_line_string_single_coordinate_rejected(
        self, invalid_multi_line_string_single_coord
    ):
        """Test MultiLineString with LineString having only one coordinate is rejected.

        According to RFC 7946 Section 3.1.4, LineString must have at least 2 coordinates.
        """
        schema = MultiLineStringSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_multi_line_string_single_coord)

        error_str = str(exc_info.value)
        assert "at least 2 coordinates" in error_str or "LineString must have" in error_str
        assert "RFC 7946" in error_str or "Section 3.1.4" in error_str

    def test_multi_line_string_empty_linestring_rejected(self):
        """Test MultiLineString with empty LineString is rejected."""
        data = {
            "type": "MultiLineString",
            "coordinates": [[]],  # Empty LineString
        }
        schema = MultiLineStringSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "at least 2 coordinates" in error_str or "LineString must have" in error_str

    def test_multi_line_string_mixed_valid_invalid_rejected(self):
        """Test MultiLineString with mix of valid and invalid LineStrings is rejected."""
        data = {
            "type": "MultiLineString",
            "coordinates": [
                [[0, 0], [1, 1]],  # Valid (2 coordinates)
                [[2, 2]],  # Invalid (1 coordinate)
            ],
        }
        schema = MultiLineStringSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "at least 2 coordinates" in error_str or "LineString must have" in error_str

    def test_multi_line_string_minimal_valid(self):
        """Test MultiLineString with minimal valid LineStrings (2 coordinates each)."""
        data = {
            "type": "MultiLineString",
            "coordinates": [
                [[0, 0], [1, 1]],  # Minimal valid LineString
                [[2, 2], [3, 3]],  # Another minimal valid LineString
            ],
        }
        schema = MultiLineStringSchema()
        mls_data = schema.load(data)
        assert mls_data["type"] == MULTI_LINE_STRING
        assert len(mls_data["coordinates"]) == 2
        assert len(mls_data["coordinates"][0]) == 2
        assert len(mls_data["coordinates"][1]) == 2

    def test_multi_line_string_serialization(self, valid_multi_line_string_data):
        """Test MultiLineString schema serialization to dict."""
        schema = MultiLineStringSchema()
        mls_data = schema.load(valid_multi_line_string_data)
        serialized = schema.dump(mls_data)

        assert serialized["type"] == "MultiLineString"
        assert len(serialized["coordinates"]) == len(valid_multi_line_string_data["coordinates"])
        # Verify structure matches input
        for idx, line in enumerate(serialized["coordinates"]):
            assert len(line) == len(valid_multi_line_string_data["coordinates"][idx])

    def test_multi_line_string_json_serialization(self, valid_multi_line_string_data):
        """Test MultiLineString schema JSON serialization."""
        schema = MultiLineStringSchema()
        mls_data = schema.load(valid_multi_line_string_data)
        json_str = schema.dumps(mls_data)

        assert '"type":"MultiLineString"' in json_str or '"type": "MultiLineString"' in json_str
        assert str(valid_multi_line_string_data["coordinates"][0][0][0]) in json_str

    def test_multi_line_string_from_json(self, valid_multi_line_string_data):
        """Test creating MultiLineString from JSON string."""
        json_str = json.dumps(valid_multi_line_string_data)
        schema = MultiLineStringSchema()
        mls_data = schema.loads(json_str)

        assert mls_data["type"] == MULTI_LINE_STRING
        assert len(mls_data["coordinates"]) == len(valid_multi_line_string_data["coordinates"])

    def test_multi_line_string_with_bbox(self, valid_multi_line_string_data, bbox_2d):
        """Test MultiLineString with bounding box."""
        data = {**valid_multi_line_string_data, "bbox": bbox_2d}
        schema = MultiLineStringSchema()
        mls_data = schema.load(data)

        assert mls_data["bbox"] == bbox_2d
        assert mls_data["type"] == MULTI_LINE_STRING
