import json

from marshmallow_geojson import MultiPolygonSchema
from marshmallow_geojson.object_type import MULTI_POLYGON


class TestMultiPolygonSchema:
    def test_loads_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data
        data_text = json.dumps(multi_polygon_dc)

        mp_schema = MultiPolygonSchema()
        mp_data = mp_schema.loads(data_text)

        coordinates = mp_data['coordinates']
        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate
                    assert multi_polygon_dc[
                               'coordinates'
                           ][mp_list_key][mp_item_key][mpl_key] == [lon, lat]

        assert multi_polygon_dc['type'] == mp_data['type']

    def test_schema_type(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data
        data_text = json.dumps(multi_polygon_dc)

        mp_schema = MultiPolygonSchema()
        mp_data = mp_schema.loads(data_text)
        assert MULTI_POLYGON == mp_data['type']
