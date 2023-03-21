import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import LineStringSchema
from marshmallow_geojson.object_type import LINE_STRING


class TestLineStringSchema:
    def test_loads_schema(self, get_line_string_data):
        line_string_dc = get_line_string_data
        data_text = json.dumps(line_string_dc)

        ls_schema = LineStringSchema()
        ls_data = ls_schema.loads(data_text)

        coordinates = ls_data['coordinates']
        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert line_string_dc['coordinates'][lsi_key] == [lon, lat]

        assert line_string_dc['type'] == ls_data['type']

    def test_loads_many_schema(self, get_line_string_data):
        line_string_dc = get_line_string_data
        data_text = json.dumps([line_string_dc])

        ls_schema = LineStringSchema(many=True)
        ls_data_list = ls_schema.loads(data_text)

        assert len(ls_data_list) == 1
        ls_data = ls_data_list[0]

        coordinates = ls_data['coordinates']
        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert line_string_dc['coordinates'][lsi_key] == [lon, lat]

        assert line_string_dc['type'] == ls_data['type']

    def test_load_schema(self, get_line_string_data):
        line_string_dc = get_line_string_data

        ls_schema = LineStringSchema()
        ls_data = ls_schema.load(line_string_dc)

        coordinates = ls_data['coordinates']
        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert line_string_dc['coordinates'][lsi_key] == [lon, lat]

        assert line_string_dc['type'] == ls_data['type']

    def test_load_many_schema(self, get_line_string_data):
        line_string_dc = get_line_string_data

        ls_schema = LineStringSchema(many=True)
        ls_data_list = ls_schema.load([line_string_dc])

        assert len(ls_data_list) == 1
        ls_data = ls_data_list[0]

        coordinates = ls_data['coordinates']
        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert line_string_dc['coordinates'][lsi_key] == [lon, lat]

        assert line_string_dc['type'] == ls_data['type']

    def test_dumps_schema(self, get_line_string_data):
        line_string_dc = get_line_string_data
        data_text = json.dumps(line_string_dc)

        ls_schema = LineStringSchema()
        ls_data_text = ls_schema.dumps(line_string_dc)

        assert json.loads(data_text) == json.loads(ls_data_text)

    def test_dumps_many_schema(self, get_line_string_data):
        line_string_dc = get_line_string_data
        data_text = json.dumps([line_string_dc])

        ls_schema = LineStringSchema(many=True)
        ls_data_text = ls_schema.dumps([line_string_dc])

        assert json.loads(data_text) == json.loads(ls_data_text)

    def test_dump_schema(self, get_line_string_data):
        line_string_dc = get_line_string_data

        ls_schema = LineStringSchema()
        ls_data = ls_schema.dump(line_string_dc)

        coordinates = ls_data['coordinates']
        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert line_string_dc['coordinates'][lsi_key] == [lon, lat]

        assert line_string_dc['type'] == ls_data['type']

    def test_dump_many_schema(self, get_line_string_data):
        line_string_dc = get_line_string_data

        ls_schema = LineStringSchema(many=True)
        ls_data_list = ls_schema.dump([line_string_dc])

        assert len(ls_data_list) == 1
        ls_data = ls_data_list[0]

        coordinates = ls_data['coordinates']
        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert line_string_dc['coordinates'][lsi_key] == [lon, lat]

        assert line_string_dc['type'] == ls_data['type']

    def test_schema_type(self, get_line_string_data):
        line_string_dc = get_line_string_data
        data_text = json.dumps(line_string_dc)

        ls_schema = LineStringSchema()
        ls_data = ls_schema.loads(data_text)
        assert LINE_STRING == ls_data['type']

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        ls_schema = LineStringSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid line string type',
        ):
            ls_schema.loads(data_text)
