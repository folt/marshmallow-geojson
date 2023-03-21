import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import MultiLineStringSchema
from marshmallow_geojson.object_type import MULTI_LINE_STRING


class TestMultiLineStringSchema:
    def test_loads_schema(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data
        data_text = json.dumps(multi_line_string_dc)

        mls_schema = MultiLineStringSchema()
        mls_data = mls_schema.loads(data_text)

        coordinates = mls_data['coordinates']
        for mlsi_key, mls_item in enumerate(coordinates):
            for mls_key, mls_coordinate in enumerate(mls_item):
                lon, lat = mls_coordinate
                coord = multi_line_string_dc['coordinates'][mlsi_key][mls_key]
                assert coord == [lon, lat]

        assert multi_line_string_dc['type'] == mls_data['type']

    def test_loads_many_schema(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data
        data_text = json.dumps([multi_line_string_dc])

        mls_schema = MultiLineStringSchema(many=True)
        mls_data_list = mls_schema.loads(data_text)

        assert len(mls_data_list) == 1
        mls_data = mls_data_list[0]

        coordinates = mls_data['coordinates']
        for mlsi_key, mls_item in enumerate(coordinates):
            for mls_key, mls_coordinate in enumerate(mls_item):
                lon, lat = mls_coordinate
                coord = multi_line_string_dc['coordinates'][mlsi_key][mls_key]
                assert coord == [lon, lat]

        assert multi_line_string_dc['type'] == mls_data['type']

    def test_load_schema(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data

        mls_schema = MultiLineStringSchema()
        mls_data = mls_schema.load(multi_line_string_dc)

        coordinates = mls_data['coordinates']
        for mlsi_key, mls_item in enumerate(coordinates):
            for mls_key, mls_coordinate in enumerate(mls_item):
                lon, lat = mls_coordinate
                coord = multi_line_string_dc['coordinates'][mlsi_key][mls_key]
                assert coord == [lon, lat]

        assert multi_line_string_dc['type'] == mls_data['type']

    def test_load_many_schema(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data

        mls_schema = MultiLineStringSchema(many=True)
        mls_data_list = mls_schema.load([multi_line_string_dc])

        assert len(mls_data_list) == 1
        mls_data = mls_data_list[0]

        coordinates = mls_data['coordinates']
        for mlsi_key, mls_item in enumerate(coordinates):
            for mls_key, mls_coordinate in enumerate(mls_item):
                lon, lat = mls_coordinate
                coord = multi_line_string_dc['coordinates'][mlsi_key][mls_key]
                assert coord == [lon, lat]

        assert multi_line_string_dc['type'] == mls_data['type']

    def test_dumps_schema(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data
        data_text = json.dumps(multi_line_string_dc)

        mls_schema = MultiLineStringSchema()
        mls_data_text = mls_schema.dumps(multi_line_string_dc)

        assert json.loads(data_text) == json.loads(mls_data_text)

    def test_dumps_many_schema(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data
        data_text = json.dumps([multi_line_string_dc])

        mls_schema = MultiLineStringSchema(many=True)
        mls_data_text = mls_schema.dumps([multi_line_string_dc])

        assert json.loads(data_text) == json.loads(mls_data_text)

    def test_dump_schema(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data

        mls_schema = MultiLineStringSchema()
        mls_data = mls_schema.dump(multi_line_string_dc)

        coordinates = mls_data['coordinates']
        for mlsi_key, mls_item in enumerate(coordinates):
            for mls_key, mls_coordinate in enumerate(mls_item):
                lon, lat = mls_coordinate
                coord = multi_line_string_dc['coordinates'][mlsi_key][mls_key]
                assert coord == [lon, lat]

        assert multi_line_string_dc['type'] == mls_data['type']

    def test_dump_many_schema(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data

        mls_schema = MultiLineStringSchema(many=True)
        mls_data_list = mls_schema.dump([multi_line_string_dc])

        assert len(mls_data_list) == 1
        mls_data = mls_data_list[0]

        coordinates = mls_data['coordinates']
        for mlsi_key, mls_item in enumerate(coordinates):
            for mls_key, mls_coordinate in enumerate(mls_item):
                lon, lat = mls_coordinate
                coord = multi_line_string_dc['coordinates'][mlsi_key][mls_key]
                assert coord == [lon, lat]

        assert multi_line_string_dc['type'] == mls_data['type']

    def test_schema_type(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data
        data_text = json.dumps(multi_line_string_dc)

        mls_schema = MultiLineStringSchema()
        mls_data = mls_schema.loads(data_text)
        assert MULTI_LINE_STRING == mls_data['type']

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        mls_schema = MultiLineStringSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid multi line string string type',
        ):
            mls_schema.loads(data_text)
