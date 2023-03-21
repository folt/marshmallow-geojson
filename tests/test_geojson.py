import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import GeoJSONSchema
from marshmallow_geojson.object_type import GeoJSONType


class TestGeoJSONSchema:
    def test_loads_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        g_schema = GeoJSONSchema()
        g_data = g_schema.loads(data_text)

        assert point_dc['type'] == g_data['type']

    def test_loads_many_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps([point_dc])

        g_schema = GeoJSONSchema(many=True)
        g_data_list = g_schema.loads(data_text)

        assert len(g_data_list) == 1
        g_data = g_data_list[0]

        assert point_dc['type'] == g_data['type']

    def test_load_schema(self, get_point_data):
        point_dc = get_point_data

        g_schema = GeoJSONSchema()
        g_data = g_schema.load(point_dc)

        assert point_dc['type'] == g_data['type']

    def test_load_many_schema(self, get_point_data):
        point_dc = get_point_data

        g_schema = GeoJSONSchema(many=True)
        g_data_list = g_schema.load([point_dc])

        assert len(g_data_list) == 1
        g_data = g_data_list[0]

        assert point_dc['type'] == g_data['type']

    def test_dumps_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        g_schema = GeoJSONSchema()
        g_data_text = g_schema.dumps(point_dc)

        assert json.loads(data_text) == json.loads(g_data_text)

    def test_dumps_many_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps([point_dc])

        g_schema = GeoJSONSchema(many=True)
        g_data_text = g_schema.dumps([point_dc])

        assert json.loads(data_text) == json.loads(g_data_text)

    def test_dump_schema(self, get_point_data):
        point_dc = get_point_data

        g_schema = GeoJSONSchema()
        g_data = g_schema.dump(point_dc)

        assert point_dc['type'] == g_data['type']

    def test_dump_many_schema(self, get_point_data):
        point_dc = get_point_data

        g_schema = GeoJSONSchema(many=True)
        g_data_list = g_schema.dump([point_dc])

        assert len(g_data_list) == 1
        g_data = g_data_list[0]

        assert point_dc['type'] == g_data['type']

    def test_schema_type(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        g_schema = GeoJSONSchema()
        g_data = g_schema.loads(data_text)
        assert g_data['type'] in [g_type.value for g_type in GeoJSONType]

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        point_dc['type'] = 'NotPoint'
        data_text = json.dumps(point_dc)

        g_schema = GeoJSONSchema()
        with pytest.raises(
            ValidationError,
            match='Unknown object class for NotPoint.',
        ):
            g_schema.loads(data_text)

    def test_schema_list_and_many_or_raise(self, get_point_data):
        point_dc = get_point_data

        data_text = json.dumps(point_dc)
        g_schema = GeoJSONSchema(many=True)
        with pytest.raises(
            ValidationError,
            match='Invalid input type.',
        ):
            g_schema.loads(data_text)

        data_text = json.dumps([point_dc])
        g_schema = GeoJSONSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid input type.',
        ):
            g_schema.loads(data_text)
