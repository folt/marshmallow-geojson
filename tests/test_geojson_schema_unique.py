"""Tests for unique GeoJSONSchema functionality not present in pydantic-geojson.

This module tests features that are unique to marshmallow-geojson:
- Universal GeoJSONSchema for all GeoJSON object types
- GeometriesSchema for all geometry types
- Marshmallow-specific parameters (only, exclude, partial, unknown)
- get_schema() method
- Mixed object types in many=True mode
"""

import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import GeoJSONSchema, GeometriesSchema


class TestGeoJSONSchemaUniversal:
    """Test GeoJSONSchema with all GeoJSON object types."""

    def test_load_point(self, valid_point_data):
        """Test loading Point geometry."""
        schema = GeoJSONSchema()
        result = schema.load(valid_point_data)

        assert result["type"] == "Point"
        assert result["coordinates"] == valid_point_data["coordinates"]

    def test_load_linestring(self, valid_linestring_data):
        """Test loading LineString geometry."""
        schema = GeoJSONSchema()
        result = schema.load(valid_linestring_data)

        assert result["type"] == "LineString"
        assert len(result["coordinates"]) == len(valid_linestring_data["coordinates"])

    def test_load_polygon(self, valid_polygon_data):
        """Test loading Polygon geometry."""
        schema = GeoJSONSchema()
        result = schema.load(valid_polygon_data)

        assert result["type"] == "Polygon"
        assert len(result["coordinates"]) == len(valid_polygon_data["coordinates"])

    def test_load_feature(self, valid_feature_point_geometry):
        """Test loading Feature object."""
        schema = GeoJSONSchema()
        result = schema.load(valid_feature_point_geometry)

        assert result["type"] == "Feature"
        assert result["geometry"] is not None
        assert result["geometry"]["type"] == "Point"

    def test_load_feature_collection(self, valid_feature_collection_data):
        """Test loading FeatureCollection object."""
        schema = GeoJSONSchema()
        result = schema.load(valid_feature_collection_data)

        assert result["type"] == "FeatureCollection"
        assert len(result["features"]) == len(valid_feature_collection_data["features"])

    def test_load_geometry_collection(self, valid_geometry_collection_data):
        """Test loading GeometryCollection object."""
        schema = GeoJSONSchema()
        result = schema.load(valid_geometry_collection_data)

        assert result["type"] == "GeometryCollection"
        assert len(result["geometries"]) == len(valid_geometry_collection_data["geometries"])

    def test_load_all_geometry_types(self, geometry_fixtures):
        """Test loading all geometry types with GeoJSONSchema."""
        schema = GeoJSONSchema()
        for geo_type, data in geometry_fixtures.items():
            result = schema.load(data)
            assert result["type"] == geo_type

    def test_load_feature_type(self, valid_feature_point_geometry):
        """Test loading Feature type with GeoJSONSchema."""
        schema = GeoJSONSchema()
        result = schema.load(valid_feature_point_geometry)
        assert result["type"] == "Feature"

    def test_load_feature_collection_type(self, valid_feature_collection_data):
        """Test loading FeatureCollection type with GeoJSONSchema."""
        schema = GeoJSONSchema()
        result = schema.load(valid_feature_collection_data)
        assert result["type"] == "FeatureCollection"

    def test_load_mixed_types_many(
        self, valid_point_data, valid_linestring_data, valid_feature_point_geometry
    ):
        """Test loading mixed GeoJSON types in many=True mode."""
        schema = GeoJSONSchema(many=True)
        mixed_data = [
            valid_point_data,
            valid_linestring_data,
            valid_feature_point_geometry,
        ]

        results = schema.load(mixed_data)

        assert len(results) == 3
        assert results[0]["type"] == "Point"
        assert results[1]["type"] == "LineString"
        assert results[2]["type"] == "Feature"

    def test_dump_mixed_types_many(
        self, valid_point_data, valid_linestring_data, valid_feature_point_geometry
    ):
        """Test dumping mixed GeoJSON types in many=True mode."""
        schema = GeoJSONSchema(many=True)
        mixed_data = [
            valid_point_data,
            valid_linestring_data,
            valid_feature_point_geometry,
        ]

        results = schema.dump(mixed_data)

        assert len(results) == 3
        assert results[0]["type"] == "Point"
        assert results[1]["type"] == "LineString"
        assert results[2]["type"] == "Feature"


class TestGeoJSONSchemaGetSchema:
    """Test get_schema() method."""

    def test_get_schema_point(self):
        """Test getting Point schema."""
        schema = GeoJSONSchema()
        point_schema = schema.get_schema("Point")

        assert point_schema == schema.point_schema

    def test_get_schema_feature(self):
        """Test getting Feature schema."""
        schema = GeoJSONSchema()
        feature_schema = schema.get_schema("Feature")

        assert feature_schema == schema.feature_schema

    def test_get_schema_invalid_type(self):
        """Test getting schema for invalid type raises ValidationError."""
        schema = GeoJSONSchema()

        with pytest.raises(ValidationError) as exc_info:
            schema.get_schema("InvalidType")

        assert "Unknown object class for InvalidType" in str(exc_info.value)

    @pytest.mark.parametrize(
        "object_type",
        [
            "Point",
            "MultiPoint",
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
            "GeometryCollection",
            "Feature",
            "FeatureCollection",
        ],
    )
    def test_get_schema_all_types(self, object_type):
        """Test getting schema for all valid types."""
        schema = GeoJSONSchema()
        result_schema = schema.get_schema(object_type)

        assert result_schema is not None


class TestGeoJSONSchemaMarshmallowParams:
    """Test marshmallow-specific parameters."""

    def test_only_parameter(self, valid_point_data):
        """Test using only parameter to include specific fields."""
        # Note: only/exclude work with direct schemas, not GeoJSONSchema
        # which creates nested schemas dynamically
        from marshmallow_geojson import PointSchema

        schema = PointSchema(only=("type", "coordinates"))
        result = schema.load(valid_point_data)

        assert "type" in result
        assert "coordinates" in result

    def test_exclude_parameter(self, valid_point_data):
        """Test using exclude parameter to exclude specific fields."""
        # Note: only/exclude work with direct schemas, not GeoJSONSchema
        # which creates nested schemas dynamically
        from marshmallow_geojson import PointSchema

        schema = PointSchema(exclude=("bbox",))
        result = schema.load(valid_point_data)

        assert "type" in result
        assert "coordinates" in result
        # bbox is excluded if present

    def test_partial_parameter(self, valid_feature_point_geometry):
        """Test using partial parameter to allow partial data."""
        schema = GeoJSONSchema(partial=True)
        # Remove optional fields to test partial loading
        partial_data = {
            "type": "Feature",
            "geometry": valid_feature_point_geometry["geometry"],
            # properties is required but can be None
        }

        # With partial=True, we can load without properties
        result = schema.load(partial_data, partial=("properties",))
        assert result["type"] == "Feature"
        assert result["geometry"] is not None

    def test_unknown_exclude(self, valid_point_data):
        """Test unknown='exclude' to ignore unknown fields."""
        schema = GeoJSONSchema(unknown="exclude")
        data_with_extra = {**valid_point_data, "extra_field": "extra_value"}

        result = schema.load(data_with_extra)

        assert "type" in result
        assert "coordinates" in result
        assert "extra_field" not in result

    def test_unknown_raise(self, valid_point_data):
        """Test unknown='raise' to raise error on unknown fields."""
        schema = GeoJSONSchema(unknown="raise")
        data_with_extra = {**valid_point_data, "extra_field": "extra_value"}

        with pytest.raises(ValidationError):
            schema.load(data_with_extra)

    def test_load_only_parameter(self, valid_feature_point_geometry):
        """Test using load_only parameter."""
        # Use load_only for properties field which is less critical for dumping
        schema = GeoJSONSchema(load_only=("properties",))
        result = schema.load(valid_feature_point_geometry)

        assert "properties" in result
        # When dumping, load_only fields should not appear
        dumped = schema.dump(result)
        assert "properties" not in dumped
        assert "type" in dumped
        assert "geometry" in dumped

    def test_dump_only_parameter(self, valid_point_data):
        """Test using dump_only parameter."""
        # Note: dump_only is less common for GeoJSON, but we test the functionality
        # In practice, this would be used for computed fields
        schema = GeoJSONSchema(dump_only=("type",))
        # type is always present, so this mainly tests the parameter works
        result = schema.load(valid_point_data)

        assert "type" in result
        assert "coordinates" in result


class TestGeometriesSchema:
    """Test GeometriesSchema for geometry-only objects."""

    def test_load_point(self, valid_point_data):
        """Test loading Point with GeometriesSchema."""
        schema = GeometriesSchema()
        result = schema.load(valid_point_data)

        assert result["type"] == "Point"
        assert result["coordinates"] == valid_point_data["coordinates"]

    def test_load_linestring(self, valid_linestring_data):
        """Test loading LineString with GeometriesSchema."""
        schema = GeometriesSchema()
        result = schema.load(valid_linestring_data)

        assert result["type"] == "LineString"
        assert len(result["coordinates"]) == len(valid_linestring_data["coordinates"])

    def test_load_polygon(self, valid_polygon_data):
        """Test loading Polygon with GeometriesSchema."""
        schema = GeometriesSchema()
        result = schema.load(valid_polygon_data)

        assert result["type"] == "Polygon"
        assert len(result["coordinates"]) == len(valid_polygon_data["coordinates"])

    def test_load_multi_point(self, valid_multi_point_data):
        """Test loading MultiPoint with GeometriesSchema."""
        schema = GeometriesSchema()
        result = schema.load(valid_multi_point_data)

        assert result["type"] == "MultiPoint"
        assert len(result["coordinates"]) == len(valid_multi_point_data["coordinates"])

    def test_load_mixed_geometries_many(
        self, valid_point_data, valid_linestring_data, valid_polygon_data
    ):
        """Test loading mixed geometry types in many=True mode."""
        schema = GeometriesSchema(many=True)
        mixed_data = [
            valid_point_data,
            valid_linestring_data,
            valid_polygon_data,
        ]

        results = schema.load(mixed_data)

        assert len(results) == 3
        assert results[0]["type"] == "Point"
        assert results[1]["type"] == "LineString"
        assert results[2]["type"] == "Polygon"

    def test_load_feature_rejected(self, valid_feature_point_geometry):
        """Test that GeometriesSchema rejects Feature objects."""
        schema = GeometriesSchema()

        with pytest.raises(ValidationError) as exc_info:
            schema.load(valid_feature_point_geometry)

        assert "Unknown object class" in str(exc_info.value)

    def test_load_feature_collection_rejected(self, valid_feature_collection_data):
        """Test that GeometriesSchema rejects FeatureCollection objects."""
        schema = GeometriesSchema()

        with pytest.raises(ValidationError) as exc_info:
            schema.load(valid_feature_collection_data)

        assert "Unknown object class" in str(exc_info.value)

    def test_get_schema_point(self):
        """Test getting Point schema from GeometriesSchema."""
        schema = GeometriesSchema()
        point_schema = schema.get_schema("Point")

        assert point_schema == schema.point_schema

    def test_get_schema_invalid_geometry(self):
        """Test getting schema for invalid geometry type."""
        schema = GeometriesSchema()

        with pytest.raises(ValidationError) as exc_info:
            schema.get_schema("Feature")

        assert "Unknown object class for Feature" in str(exc_info.value)


class TestGeoJSONSchemaLoadsDumps:
    """Test loads() and dumps() methods with various types."""

    def test_loads_point(self, valid_point_data):
        """Test loads() with Point JSON string."""
        schema = GeoJSONSchema()
        json_str = json.dumps(valid_point_data)

        result = schema.loads(json_str)

        assert result["type"] == "Point"
        assert result["coordinates"] == valid_point_data["coordinates"]

    def test_loads_feature(self, valid_feature_point_geometry):
        """Test loads() with Feature JSON string."""
        schema = GeoJSONSchema()
        json_str = json.dumps(valid_feature_point_geometry)

        result = schema.loads(json_str)

        assert result["type"] == "Feature"
        assert result["geometry"] is not None

    def test_dumps_point(self, valid_point_data):
        """Test dumps() with Point object."""
        schema = GeoJSONSchema()

        json_str = schema.dumps(valid_point_data)
        parsed = json.loads(json_str)

        assert parsed["type"] == "Point"
        assert parsed["coordinates"] == valid_point_data["coordinates"]

    def test_loads_many_mixed(
        self, valid_point_data, valid_linestring_data, valid_feature_point_geometry
    ):
        """Test loads() with mixed types in many=True mode."""
        schema = GeoJSONSchema(many=True)
        mixed_data = [
            valid_point_data,
            valid_linestring_data,
            valid_feature_point_geometry,
        ]
        json_str = json.dumps(mixed_data)

        results = schema.loads(json_str)

        assert len(results) == 3
        assert results[0]["type"] == "Point"
        assert results[1]["type"] == "LineString"
        assert results[2]["type"] == "Feature"

    def test_dumps_many_mixed(
        self, valid_point_data, valid_linestring_data, valid_feature_point_geometry
    ):
        """Test dumps() with mixed types in many=True mode."""
        schema = GeoJSONSchema(many=True)
        mixed_data = [
            valid_point_data,
            valid_linestring_data,
            valid_feature_point_geometry,
        ]

        json_str = schema.dumps(mixed_data)
        parsed = json.loads(json_str)

        assert len(parsed) == 3
        assert parsed[0]["type"] == "Point"
        assert parsed[1]["type"] == "LineString"
        assert parsed[2]["type"] == "Feature"
