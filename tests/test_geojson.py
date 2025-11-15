"""Tests for GeoJSONSchema."""

import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import GeoJSONSchema
from marshmallow_geojson.object_type import GeoJSONType


class TestGeoJSONSchema:
    """Test suite for GeoJSONSchema validation and serialization."""

    def test_loads_schema(self, valid_point_data):
        """Test loading GeoJSON from JSON string."""
        data_text = json.dumps(valid_point_data)

        g_schema = GeoJSONSchema()
        g_data = g_schema.loads(data_text)

        assert valid_point_data["type"] == g_data["type"]
        assert valid_point_data["coordinates"] == g_data["coordinates"]

    def test_loads_many_schema(self, valid_point_data):
        """Test loading multiple GeoJSON objects from JSON string."""
        data_text = json.dumps([valid_point_data])

        g_schema = GeoJSONSchema(many=True)
        g_data_list = g_schema.loads(data_text)

        assert len(g_data_list) == 1
        g_data = g_data_list[0]

        assert valid_point_data["type"] == g_data["type"]
        assert valid_point_data["coordinates"] == g_data["coordinates"]

    def test_load_schema(self, valid_point_data):
        """Test loading GeoJSON from dictionary."""
        g_schema = GeoJSONSchema()
        g_data = g_schema.load(valid_point_data)

        assert valid_point_data["type"] == g_data["type"]
        assert valid_point_data["coordinates"] == g_data["coordinates"]

    def test_load_many_schema(self, valid_point_data):
        """Test loading multiple GeoJSON objects from list."""
        g_schema = GeoJSONSchema(many=True)
        g_data_list = g_schema.load([valid_point_data])

        assert len(g_data_list) == 1
        g_data = g_data_list[0]

        assert valid_point_data["type"] == g_data["type"]
        assert valid_point_data["coordinates"] == g_data["coordinates"]

    def test_dumps_schema(self, valid_point_data):
        """Test dumping GeoJSON to JSON string."""
        g_schema = GeoJSONSchema()
        g_data_text = g_schema.dumps(valid_point_data)

        expected_text = json.dumps(valid_point_data)
        assert json.loads(expected_text) == json.loads(g_data_text)

    def test_dumps_many_schema(self, valid_point_data):
        """Test dumping multiple GeoJSON objects to JSON string."""
        g_schema = GeoJSONSchema(many=True)
        g_data_text = g_schema.dumps([valid_point_data])

        expected_text = json.dumps([valid_point_data])
        assert json.loads(expected_text) == json.loads(g_data_text)

    def test_dump_schema(self, valid_point_data):
        """Test dumping GeoJSON to dictionary."""
        g_schema = GeoJSONSchema()
        g_data = g_schema.dump(valid_point_data)

        assert valid_point_data["type"] == g_data["type"]
        assert valid_point_data["coordinates"] == g_data["coordinates"]

    def test_dump_many_schema(self, valid_point_data):
        """Test dumping multiple GeoJSON objects to list."""
        g_schema = GeoJSONSchema(many=True)
        g_data_list = g_schema.dump([valid_point_data])

        assert len(g_data_list) == 1
        g_data = g_data_list[0]

        assert valid_point_data["type"] == g_data["type"]
        assert valid_point_data["coordinates"] == g_data["coordinates"]

    def test_schema_type(self, valid_point_data):
        """Test that loaded GeoJSON type is valid."""
        data_text = json.dumps(valid_point_data)

        g_schema = GeoJSONSchema()
        g_data = g_schema.loads(data_text)
        assert g_data["type"] in [g_type.value for g_type in GeoJSONType]

    def test_schema_type_error(self, valid_point_data):
        """Test that invalid type raises ValidationError."""
        invalid_data = valid_point_data.copy()
        invalid_data["type"] = "NotPoint"
        data_text = json.dumps(invalid_data)

        g_schema = GeoJSONSchema()
        with pytest.raises(
            ValidationError,
            match="Unknown object class for NotPoint.",
        ):
            g_schema.loads(data_text)

    def test_schema_list_and_many_or_raise(self, valid_point_data):
        """Test that mismatched list/many flags raise ValidationError."""
        data_text = json.dumps(valid_point_data)
        g_schema = GeoJSONSchema(many=True)
        with pytest.raises(
            ValidationError,
            match="Invalid input type.",
        ):
            g_schema.loads(data_text)

        data_text = json.dumps([valid_point_data])
        g_schema = GeoJSONSchema()
        with pytest.raises(
            ValidationError,
            match="Invalid input type.",
        ):
            g_schema.loads(data_text)
