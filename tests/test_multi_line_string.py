import json

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

                assert multi_line_string_dc[
                           'coordinates'
                       ][mlsi_key][mls_key] == [lon, lat]

        assert multi_line_string_dc['type'] == mls_data['type']

    def test_schema_type(self, get_multi_line_string_data):
        multi_line_string_dc = get_multi_line_string_data
        data_text = json.dumps(multi_line_string_dc)

        mls_schema = MultiLineStringSchema()
        mls_data = mls_schema.loads(data_text)
        assert MULTI_LINE_STRING == mls_data['type']
