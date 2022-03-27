import json

from marshmallow_geojson import PointSchema
from marshmallow_geojson.object_type import POINT

data = {'type': 'Point', 'coordinates': [-105.01621, 39.57422]}
data_text = json.dumps(data)


class TestPointSchema:
    def test_loads_schema(self):
        p_schema = PointSchema()
        p_data = p_schema.loads(data_text)

        lon, lat = p_data['coordinates']
        assert data['type'] == p_data['type']
        assert data['coordinates'] == [lon, lat]

    def test_schema_type(self):
        p_schema = PointSchema()
        p_data = p_schema.loads(data_text)
        assert POINT == p_data['type']
