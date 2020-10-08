import ujson
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
data_text = ujson.dumps(data)


class TestPointSchemaStringType:
    def test_loads_schema(self):
        point_schema = PolygonSchema()
        point_data = point_schema.loads(data_text)
        for pi_key, polygon_item in enumerate(point_data['coordinates']):
            for pl_key, polygon_coordinate in enumerate(polygon_item):
                lon, lat = polygon_coordinate
                assert data['coordinates'][pi_key][pl_key] == [lon, lat]

        assert data['type'] == point_data['type']

    def test_schema_type(self):
        point_schema = PolygonSchema()
        point_data = point_schema.loads(data_text)
        assert POLYGON == point_data['type']
