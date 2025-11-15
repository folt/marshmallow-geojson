"""Tests for FeatureSchema."""

import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import FeatureSchema
from marshmallow_geojson.object_type import FEATURE


class TestFeatureSchema:
    """Test suite for FeatureSchema validation and serialization."""

    def test_valid_feature_with_all_fields(self, valid_feature_all_fields):
        """Test creating a Feature with all fields populated."""
        schema = FeatureSchema()
        f_data = schema.load(valid_feature_all_fields)

        assert f_data["type"] == FEATURE
        assert f_data["geometry"] is not None
        assert f_data["geometry"]["type"] == valid_feature_all_fields["geometry"]["type"]
        assert isinstance(f_data["properties"], dict)
        assert f_data["properties"] == valid_feature_all_fields["properties"]
        assert f_data["id"] == valid_feature_all_fields["id"]

    def test_valid_feature_minimal(self, valid_feature_type_only):
        """Test creating a Feature with only required fields."""
        schema = FeatureSchema()
        f_data = schema.load(valid_feature_type_only)

        assert f_data["type"] == FEATURE
        assert f_data["geometry"] is None
        assert f_data["properties"] is None
        assert f_data.get("id") is None

    def test_feature_with_point_geometry(self, valid_feature_point_geometry):
        """Test Feature with Point geometry."""
        schema = FeatureSchema()
        f_data = schema.load(valid_feature_point_geometry)

        assert f_data["type"] == FEATURE
        assert f_data["geometry"] is not None
        assert f_data["geometry"]["type"] == "Point"
        assert f_data["properties"] == {"name": "Test Point"}

    @pytest.mark.parametrize(
        "geometry_type",
        [
            "Point",
            "MultiPoint",
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
            "GeometryCollection",
        ],
    )
    def test_feature_with_different_geometry_types(self, geometry_type, geometry_fixtures):
        """Test Feature with different geometry types."""
        data = {
            "type": "Feature",
            "geometry": geometry_fixtures[geometry_type],
            "properties": {"name": f"Test {geometry_type}"},
        }

        schema = FeatureSchema()
        f_data = schema.load(data)
        assert f_data["type"] == FEATURE
        assert f_data["geometry"] is not None
        assert f_data["geometry"]["type"] == geometry_type

    def test_feature_invalid_type(self, invalid_feature_wrong_type):
        """Test Feature with invalid type field."""
        schema = FeatureSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(invalid_feature_wrong_type)

        assert "Invalid feature type" in str(exc_info.value)

    def test_feature_serialization(self, valid_feature_all_fields):
        """Test Feature schema serialization to dict."""
        schema = FeatureSchema()
        f_data = schema.load(valid_feature_all_fields)
        serialized = schema.dump(f_data)

        assert serialized["type"] == "Feature"
        assert serialized["geometry"] is not None
        assert serialized["properties"] == valid_feature_all_fields["properties"]
        assert serialized["id"] == valid_feature_all_fields["id"]

    def test_feature_json_serialization(self, valid_feature_all_fields):
        """Test Feature schema JSON serialization."""
        schema = FeatureSchema()
        f_data = schema.load(valid_feature_all_fields)
        json_str = schema.dumps(f_data)

        assert '"type":"Feature"' in json_str or '"type": "Feature"' in json_str
        assert '"geometry"' in json_str
        assert '"properties"' in json_str

    def test_feature_from_json(self, valid_feature_all_fields):
        """Test creating Feature from JSON string."""
        json_str = json.dumps(valid_feature_all_fields)
        schema = FeatureSchema()
        f_data = schema.loads(json_str)

        assert f_data["type"] == FEATURE
        assert f_data["properties"] == valid_feature_all_fields["properties"]

    @pytest.mark.parametrize(
        "id_name,id_value",
        [
            ("string_id", "feature-123"),
            ("integer_id", 123),
            ("numeric_string_id", "456"),
            ("large_integer_id", 999999),
        ],
    )
    def test_feature_with_different_id_types(self, id_name, id_value, valid_feature_point_geometry):
        """Test Feature with different ID types."""
        data = {**valid_feature_point_geometry, "id": id_value}
        schema = FeatureSchema()
        f_data = schema.load(data)

        assert f_data["id"] == id_value
        assert isinstance(f_data["id"], type(id_value))

    def test_feature_with_bbox(self, valid_feature_all_fields, bbox_2d):
        """Test Feature with bounding box."""
        data = {**valid_feature_all_fields, "bbox": bbox_2d}
        schema = FeatureSchema()
        f_data = schema.load(data)

        assert f_data["bbox"] == bbox_2d
        assert f_data["type"] == FEATURE

    def test_feature_properties_validation(self, valid_feature_all_fields):
        """Test that Feature properties are correctly validated."""
        schema = FeatureSchema()
        f_data = schema.load(valid_feature_all_fields)

        assert isinstance(f_data["properties"], dict)
        assert f_data["properties"] == valid_feature_all_fields["properties"]

    def test_feature_with_geometry_collection(self, feature_with_geometry_collection):
        """Test Feature with GeometryCollection geometry."""
        schema = FeatureSchema()
        f_data = schema.load(feature_with_geometry_collection)

        assert f_data["type"] == FEATURE
        assert f_data["geometry"] is not None
        assert f_data["geometry"]["type"] == "GeometryCollection"
        assert len(f_data["geometry"]["geometries"]) == 2
        assert f_data["geometry"]["geometries"][0]["type"] == "Point"
        assert f_data["geometry"]["geometries"][1]["type"] == "LineString"
        assert f_data["properties"] == {"name": "Test GeometryCollection"}

    def test_feature_with_nested_geometry_collection(self, feature_with_nested_geometry_collection):
        """Test Feature with nested GeometryCollection in geometry."""
        schema = FeatureSchema()
        f_data = schema.load(feature_with_nested_geometry_collection)

        assert f_data["type"] == FEATURE
        assert f_data["geometry"] is not None
        assert f_data["geometry"]["type"] == "GeometryCollection"
        assert len(f_data["geometry"]["geometries"]) == 2
        assert f_data["geometry"]["geometries"][0]["type"] == "Point"
        assert f_data["geometry"]["geometries"][1]["type"] == "GeometryCollection"
        assert len(f_data["geometry"]["geometries"][1]["geometries"]) == 1

    def test_feature_with_geometry_collection_null_geometry_still_works(
        self, valid_feature_type_only
    ):
        """Test that Feature with null geometry still works after adding GeometryCollection support."""
        schema = FeatureSchema()
        f_data = schema.load(valid_feature_type_only)

        assert f_data["type"] == FEATURE
        assert f_data["geometry"] is None
        assert f_data["properties"] is None
        assert f_data.get("id") is None

    def test_feature_with_geometry_collection_serialization(self, geometry_fixtures):
        """Test Feature with GeometryCollection serialization."""
        data = {
            "type": "Feature",
            "geometry": geometry_fixtures["GeometryCollection"],
            "properties": {"name": "Test"},
        }
        schema = FeatureSchema()
        f_data = schema.load(data)
        serialized = schema.dump(f_data)

        assert serialized["type"] == "Feature"
        assert serialized["geometry"] is not None
        assert serialized["geometry"]["type"] == "GeometryCollection"
        assert len(serialized["geometry"]["geometries"]) == 1
        assert serialized["geometry"]["geometries"][0]["type"] == "Point"
