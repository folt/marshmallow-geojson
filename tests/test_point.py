import json

from marshmallow_geojson import PointSchema
from marshmallow_geojson.object_type import POINT


class TestPointSchema:
    def test_loads_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        p_schema = PointSchema()
        p_data = p_schema.loads(data_text)

        lon, lat = p_data['coordinates']
        assert point_dc['type'] == p_data['type']
        assert point_dc['coordinates'] == [lon, lat]

    def test_schema_type(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        p_schema = PointSchema()
        p_data = p_schema.loads(data_text)
        assert POINT == p_data['type']
