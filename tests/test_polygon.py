import json

from marshmallow_geojson import PolygonSchema
from marshmallow_geojson.object_type import POLYGON

data = {
    'type': 'Polygon',
    'coordinates': [
        [
            [100, 0],
            [101, 0],
            [101, 1],
            [100, 1],
            [100, 0]
        ]
    ]
}
data_text = json.dumps(data)


class TestPolygonSchema:
    def test_loads_schema(self):
        p_schema = PolygonSchema()
        p_data = p_schema.loads(data_text)

        coordinates = p_data['coordinates']
        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate
                assert data['coordinates'][pi_key][pl_key] == [lon, lat]

        assert data['type'] == p_data['type']

    def test_schema_type(self):
        p_schema = PolygonSchema()
        p_data = p_schema.loads(data_text)
        assert POLYGON == p_data['type']
