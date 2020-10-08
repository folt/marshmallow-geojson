import ujson
from marshmallow_geojson import PointSchema
from marshmallow_geojson.object_type import POINT

data = {'type': 'Point', 'coordinates': [-105.01621, 39.57422]}
data_text = ujson.dumps(data)


class TestPointSchemaStringType:
    def test_loads_schema(self):
        point_schema = PointSchema()
        point_data = point_schema.loads(data_text)
        lon, lat = point_data['coordinates']
        assert data['type'] == point_data['type']
        assert data['coordinates'] == [lon, lat]

    def test_schema_type(self):
        point_schema = PointSchema()
        point_data = point_schema.loads(data_text)
        assert POINT == point_data['type']
