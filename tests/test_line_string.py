import json

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

    def test_schema_type(self, get_line_string_data):
        line_string_dc = get_line_string_data
        data_text = json.dumps(line_string_dc)

        ls_schema = LineStringSchema()
        ls_data = ls_schema.loads(data_text)
        assert LINE_STRING == ls_data['type']
