"""Tests for type mixing validation according to RFC 7946 Section 7.1."""

from typing import Any

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import (
    FeatureCollectionSchema,
    FeatureSchema,
    GeometryCollectionSchema,
    LineStringSchema,
    MultiLineStringSchema,
    MultiPointSchema,
    MultiPolygonSchema,
    PointSchema,
    PolygonSchema,
)


class TestFeatureTypeMixing:
    """Test that Feature objects reject Geometry and FeatureCollection members."""

    def test_feature_with_coordinates_rejected(self):
        """Test that Feature with 'coordinates' member is rejected."""
        data: dict[str, Any] = {
            "type": "Feature",
            "geometry": None,
            "properties": {},
            "coordinates": [0, 0],  # Forbidden member
        }
        schema = FeatureSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "coordinates" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_feature_with_geometries_rejected(self):
        """Test that Feature with 'geometries' member is rejected."""
        data: dict[str, Any] = {
            "type": "Feature",
            "geometry": None,
            "properties": {},
            "geometries": [],  # Forbidden member
        }
        schema = FeatureSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "geometries" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_feature_with_features_rejected(self):
        """Test that Feature with 'features' member is rejected."""
        data: dict[str, Any] = {
            "type": "Feature",
            "geometry": None,
            "properties": {},
            "features": [],  # Forbidden member
        }
        schema = FeatureSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "features" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_feature_with_foreign_member_allowed(self):
        """Test that Feature with foreign member (not forbidden) is allowed."""
        data: dict[str, Any] = {
            "type": "Feature",
            "geometry": None,
            "properties": {},
            "custom_field": "value",  # Foreign member - should be allowed
        }
        # Should not raise ValidationError
        schema = FeatureSchema()
        feature_data = schema.load(data)
        assert feature_data["type"] == "Feature"


class TestFeatureCollectionTypeMixing:
    """Test that FeatureCollection objects reject Geometry and Feature members."""

    def test_feature_collection_with_coordinates_rejected(self):
        """Test that FeatureCollection with 'coordinates' member is rejected."""
        data = {
            "type": "FeatureCollection",
            "features": [],
            "coordinates": [0, 0],  # Forbidden member
        }
        schema = FeatureCollectionSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "coordinates" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_feature_collection_with_geometries_rejected(self):
        """Test that FeatureCollection with 'geometries' member is rejected."""
        data = {
            "type": "FeatureCollection",
            "features": [],
            "geometries": [],  # Forbidden member
        }
        schema = FeatureCollectionSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "geometries" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_feature_collection_with_geometry_rejected(self):
        """Test that FeatureCollection with 'geometry' member is rejected."""
        data = {
            "type": "FeatureCollection",
            "features": [],
            "geometry": {"type": "Point", "coordinates": [0, 0]},  # Forbidden member
        }
        schema = FeatureCollectionSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "geometry" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_feature_collection_with_properties_rejected(self):
        """Test that FeatureCollection with 'properties' member is rejected."""
        data = {
            "type": "FeatureCollection",
            "features": [],
            "properties": {},  # Forbidden member
        }
        schema = FeatureCollectionSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "properties" in error_str
        assert "RFC 7946 Section 7.1" in error_str


class TestGeometryCollectionTypeMixing:
    """Test that GeometryCollection objects reject Feature and FeatureCollection members."""

    def test_geometry_collection_with_geometry_rejected(self):
        """Test that GeometryCollection with 'geometry' member is rejected."""
        data = {
            "type": "GeometryCollection",
            "geometries": [],
            "geometry": {"type": "Point", "coordinates": [0, 0]},  # Forbidden member
        }
        schema = GeometryCollectionSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "geometry" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_geometry_collection_with_properties_rejected(self):
        """Test that GeometryCollection with 'properties' member is rejected."""
        data = {
            "type": "GeometryCollection",
            "geometries": [],
            "properties": {},  # Forbidden member
        }
        schema = GeometryCollectionSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "properties" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_geometry_collection_with_features_rejected(self):
        """Test that GeometryCollection with 'features' member is rejected."""
        data = {
            "type": "GeometryCollection",
            "geometries": [],
            "features": [],  # Forbidden member
        }
        schema = GeometryCollectionSchema()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "features" in error_str
        assert "RFC 7946 Section 7.1" in error_str


class TestGeometryTypeMixing:
    """Test that Geometry objects (Point, LineString, etc.) reject Feature and FeatureCollection members."""

    @pytest.mark.parametrize(
        "schema_class,geometry_data",
        [
            (PointSchema, {"type": "Point", "coordinates": [0, 0]}),
            (
                LineStringSchema,
                {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
            ),
            (
                PolygonSchema,
                {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
            ),
            (MultiPointSchema, {"type": "MultiPoint", "coordinates": [[0, 0], [1, 1]]}),
            (
                MultiLineStringSchema,
                {"type": "MultiLineString", "coordinates": [[[0, 0], [1, 1]]]},
            ),
            (
                MultiPolygonSchema,
                {
                    "type": "MultiPolygon",
                    "coordinates": [[[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]],
                },
            ),
        ],
    )
    def test_geometry_with_geometry_member_rejected(self, schema_class, geometry_data):
        """Test that Geometry objects with 'geometry' member are rejected."""
        data = {**geometry_data, "geometry": {"type": "Point", "coordinates": [0, 0]}}

        schema = schema_class()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "geometry" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    @pytest.mark.parametrize(
        "schema_class,geometry_data",
        [
            (PointSchema, {"type": "Point", "coordinates": [0, 0]}),
            (
                LineStringSchema,
                {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
            ),
            (
                PolygonSchema,
                {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
            ),
            (MultiPointSchema, {"type": "MultiPoint", "coordinates": [[0, 0], [1, 1]]}),
            (
                MultiLineStringSchema,
                {"type": "MultiLineString", "coordinates": [[[0, 0], [1, 1]]]},
            ),
            (
                MultiPolygonSchema,
                {
                    "type": "MultiPolygon",
                    "coordinates": [[[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]],
                },
            ),
        ],
    )
    def test_geometry_with_properties_member_rejected(self, schema_class, geometry_data):
        """Test that Geometry objects with 'properties' member are rejected."""
        data = {**geometry_data, "properties": {}}

        schema = schema_class()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "properties" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    @pytest.mark.parametrize(
        "schema_class,geometry_data",
        [
            (PointSchema, {"type": "Point", "coordinates": [0, 0]}),
            (
                LineStringSchema,
                {"type": "LineString", "coordinates": [[0, 0], [1, 1]]},
            ),
            (
                PolygonSchema,
                {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
            ),
            (MultiPointSchema, {"type": "MultiPoint", "coordinates": [[0, 0], [1, 1]]}),
            (
                MultiLineStringSchema,
                {"type": "MultiLineString", "coordinates": [[[0, 0], [1, 1]]]},
            ),
            (
                MultiPolygonSchema,
                {
                    "type": "MultiPolygon",
                    "coordinates": [[[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]],
                },
            ),
        ],
    )
    def test_geometry_with_features_member_rejected(self, schema_class, geometry_data):
        """Test that Geometry objects with 'features' member are rejected."""
        data = {**geometry_data, "features": []}

        schema = schema_class()
        with pytest.raises(ValidationError) as exc_info:
            schema.load(data)

        error_str = str(exc_info.value)
        assert "features" in error_str
        assert "RFC 7946 Section 7.1" in error_str

    def test_geometry_with_foreign_member_allowed(self):
        """Test that Geometry objects with foreign member (not forbidden) are allowed."""
        data = {
            "type": "Point",
            "coordinates": [0, 0],
            "custom_field": "value",  # Foreign member - should be allowed
        }
        # Should not raise ValidationError
        schema = PointSchema()
        point_data = schema.load(data)
        assert point_data["type"] == "Point"
