import json

from marshmallow_geojson import PolygonSchema
from marshmallow_geojson.object_type import POLYGON


class TestPolygonSchema:
    def test_loads_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data
        data_text = json.dumps(polygon_dc)

        p_schema = PolygonSchema()
        p_data = p_schema.loads(data_text)

        coordinates = p_data['coordinates']
        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate
                assert polygon_dc['coordinates'][pi_key][pl_key] == [lon, lat]

        assert polygon_dc['type'] == p_data['type']

    def test_schema_type(self, get_polygon_data):
        polygon_dc = get_polygon_data
        data_text = json.dumps(polygon_dc)

        p_schema = PolygonSchema()
        p_data = p_schema.loads(data_text)
        assert POLYGON == p_data['type']
