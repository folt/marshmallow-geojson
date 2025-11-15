"""Tests for PointSchema."""

import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import PointSchema
from marshmallow_geojson.object_type import POINT
from tests.test_utils import assert_coordinates_equal


class TestPointSchema:
    """Test suite for PointSchema validation and serialization."""

    def test_valid_point_creation(self, valid_point_data):
        """Test creating a valid Point schema."""
        schema = PointSchema()
        point_data = schema.load(valid_point_data)

        assert point_data["type"] == POINT
        assert point_data["type"] == valid_point_data["type"]
        assert_coordinates_equal(point_data["coordinates"], valid_point_data["coordinates"])

    def test_valid_point_with_altitude(self, valid_point_3d_data):
        """Test creating a Point with altitude."""
        schema = PointSchema()
        point_data = schema.load(valid_point_3d_data)

        assert point_data["type"] == POINT
        assert_coordinates_equal(point_data["coordinates"], valid_point_3d_data["coordinates"])

    @pytest.mark.parametrize(
        "name,coords",
        [
            ("lon_min", [-180, 0]),
            ("lon_max", [180, 0]),
            ("lat_min", [0, -90]),
            ("lat_max", [0, 90]),
            ("corner_sw", [-180, -90]),
            ("corner_ne", [180, 90]),
            ("corner_nw", [-180, 90]),
            ("corner_se", [180, -90]),
        ],
    )
    def test_point_boundary_coordinates(self, name, coords):
        """Test Point with coordinates at valid boundaries."""
        data = {"type": "Point", "coordinates": coords}
        schema = PointSchema()
        point_data = schema.load(data)
        assert point_data["type"] == POINT
        assert_coordinates_equal(point_data["coordinates"], coords)

    @pytest.mark.parametrize(
        "invalid_coord",
        [
            "lon_too_small",
            "lon_too_large",
            "lat_too_small",
            "lat_too_large",
        ],
    )
    def test_point_invalid_coordinates(self, invalid_coordinates, invalid_coord):
        """Test Point with invalid coordinate ranges."""
        data = {"type": "Point", "coordinates": invalid_coordinates[invalid_coord]}
        schema = PointSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert (
            "Longitude must be between -180, 180" in error_str
            or "Latitude must be between -90, 90" in error_str
        )

    def test_point_invalid_type(self, invalid_point_bad_type):
        """Test Point with invalid type field."""
        schema = PointSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_point_bad_type)

        assert "Invalid point type" in str(exc_info.value)

    def test_point_serialization(self, valid_point_data):
        """Test Point schema serialization to dict."""
        schema = PointSchema()
        point_data = schema.load(valid_point_data)
        serialized = schema.dump(point_data)

        assert serialized["type"] == "Point"
        assert_coordinates_equal(serialized["coordinates"], valid_point_data["coordinates"])

    def test_point_json_serialization(self, valid_point_data):
        """Test Point schema JSON serialization."""
        schema = PointSchema()
        point_data = schema.load(valid_point_data)
        json_str = schema.dumps(point_data)

        assert '"type":"Point"' in json_str or '"type": "Point"' in json_str
        assert str(valid_point_data["coordinates"][0]) in json_str
        assert str(valid_point_data["coordinates"][1]) in json_str

    def test_point_from_json(self, valid_point_data):
        """Test creating Point from JSON string."""
        json_str = json.dumps(valid_point_data)
        schema = PointSchema()
        point_data = schema.loads(json_str)

        assert point_data["type"] == POINT
        assert_coordinates_equal(point_data["coordinates"], valid_point_data["coordinates"])

    def test_point_with_bbox(self, valid_point_data, bbox_2d):
        """Test Point with bounding box."""
        data = {**valid_point_data, "bbox": bbox_2d}
        schema = PointSchema()
        point_data = schema.load(data)

        assert point_data["bbox"] == bbox_2d
        assert point_data["type"] == POINT

    def test_point_with_bbox_3d(self, valid_point_3d_data, bbox_3d):
        """Test Point with 3D bounding box."""
        data = {**valid_point_3d_data, "bbox": bbox_3d}
        schema = PointSchema()
        point_data = schema.load(data)

        assert point_data["bbox"] == bbox_3d
        assert point_data["type"] == POINT

    def test_point_invalid_coordinates_too_many_elements(self):
        """Test Point with coordinates having more than 3 elements."""
        data = {"type": "Point", "coordinates": [125.6, 10.1, 100.5, 200.0]}
        schema = PointSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "Position must have at most 3 elements" in error_str

    def test_point_invalid_coordinates_too_few_elements(self):
        """Test Point with coordinates having fewer than 2 elements."""
        data = {"type": "Point", "coordinates": [125.6]}
        schema = PointSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "2 or 3 elements" in error_str or "must have" in error_str
