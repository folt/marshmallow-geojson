import json

from marshmallow_geojson import MultiPointSchema
from marshmallow_geojson.object_type import MULTI_POINT


class TestMultiPointSchema:
    def test_loads_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data
        data_text = json.dumps(multi_point_dc)

        mp_schema = MultiPointSchema()
        mp_data = mp_schema.loads(data_text)

        coordinates = mp_data['coordinates']
        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item
            assert multi_point_dc['coordinates'][mpi_key] == [lon, lat]

        assert multi_point_dc['type'] == mp_data['type']

    def test_schema_type(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data
        data_text = json.dumps(multi_point_dc)

        mp_schema = MultiPointSchema()
        mp_data = mp_schema.loads(data_text)
        assert MULTI_POINT == mp_data['type']
