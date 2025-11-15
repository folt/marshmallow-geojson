"""Tests for MultiPointSchema."""

import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import MultiPointSchema
from marshmallow_geojson.object_type import MULTI_POINT
from tests.test_utils import assert_coordinates_equal


class TestMultiPointSchema:
    """Test suite for MultiPointSchema validation and serialization."""

    def test_valid_multi_point_creation(self, valid_multi_point_data):
        """Test creating a valid MultiPoint schema."""
        schema = MultiPointSchema()
        mp_data = schema.load(valid_multi_point_data)

        assert mp_data["type"] == MULTI_POINT
        assert mp_data["type"] == valid_multi_point_data["type"]
        assert len(mp_data["coordinates"]) == len(valid_multi_point_data["coordinates"])

        for idx, coord in enumerate(mp_data["coordinates"]):
            expected = valid_multi_point_data["coordinates"][idx]
            assert_coordinates_equal(coord, expected)

    def test_valid_multi_point_single(self, valid_multi_point_single):
        """Test MultiPoint with a single point."""
        schema = MultiPointSchema()
        mp_data = schema.load(valid_multi_point_single)

        assert mp_data["type"] == MULTI_POINT
        assert len(mp_data["coordinates"]) == 1

    def test_multi_point_invalid_type(self, invalid_bad_multi_point_type):
        """Test MultiPoint with invalid type field."""
        schema = MultiPointSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_bad_multi_point_type)

        assert "Invalid multi point type" in str(exc_info.value)

    def test_multi_point_serialization(self, valid_multi_point_data):
        """Test MultiPoint schema serialization to dict."""
        schema = MultiPointSchema()
        mp_data = schema.load(valid_multi_point_data)
        serialized = schema.dump(mp_data)

        assert serialized["type"] == "MultiPoint"
        assert len(serialized["coordinates"]) == len(valid_multi_point_data["coordinates"])
        # Coordinates may include None for altitude, so check first 2 elements of each coordinate
        for idx, coord in enumerate(serialized["coordinates"]):
            assert coord[:2] == valid_multi_point_data["coordinates"][idx]

    def test_multi_point_json_serialization(self, valid_multi_point_data):
        """Test MultiPoint schema JSON serialization."""
        schema = MultiPointSchema()
        mp_data = schema.load(valid_multi_point_data)
        json_str = schema.dumps(mp_data)

        assert '"type":"MultiPoint"' in json_str or '"type": "MultiPoint"' in json_str
        assert str(valid_multi_point_data["coordinates"][0][0]) in json_str

    def test_multi_point_from_json(self, valid_multi_point_data):
        """Test creating MultiPoint from JSON string."""
        json_str = json.dumps(valid_multi_point_data)
        schema = MultiPointSchema()
        mp_data = schema.loads(json_str)

        assert mp_data["type"] == MULTI_POINT
        assert len(mp_data["coordinates"]) == len(valid_multi_point_data["coordinates"])

    def test_multi_point_with_bbox(self, valid_multi_point_data, bbox_2d):
        """Test MultiPoint with bounding box."""
        data = {**valid_multi_point_data, "bbox": bbox_2d}
        schema = MultiPointSchema()
        mp_data = schema.load(data)

        assert mp_data["bbox"] == bbox_2d
        assert mp_data["type"] == MULTI_POINT

    def test_multi_point_empty(self):
        """Test MultiPoint with empty coordinates list."""
        data = {"type": "MultiPoint", "coordinates": []}
        schema = MultiPointSchema()
        mp_data = schema.load(data)

        assert mp_data["type"] == MULTI_POINT
        assert len(mp_data["coordinates"]) == 0
