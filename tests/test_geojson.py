import json

from marshmallow_geojson import GeoJSONSchema
from marshmallow_geojson.object_type import GeoJSONType

data = {'type': 'Point', 'coordinates': [-105.01621, 39.57422]}
data_text = json.dumps(data)


class TestGeoJSONSchema:
    def test_loads_schema(self):
        g_schema = GeoJSONSchema()
        g_data = g_schema.loads(data_text)

        assert data['type'] == g_data['type']

    def test_schema_type(self):
        fc_schema = GeoJSONSchema()
        fc_data = fc_schema.loads(data_text)
        assert fc_data['type'] in [g_type.value for g_type in GeoJSONType]
