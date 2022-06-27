import json

from marshmallow_geojson import GeoJSONSchema
from marshmallow_geojson.object_type import GeoJSONType


class TestGeoJSONSchema:
    def test_loads_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        g_schema = GeoJSONSchema()
        g_data = g_schema.loads(data_text)

        assert point_dc['type'] == g_data['type']

    def test_schema_type(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        fc_schema = GeoJSONSchema()
        fc_data = fc_schema.loads(data_text)
        assert fc_data['type'] in [g_type.value for g_type in GeoJSONType]
