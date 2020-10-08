import ujson
from marshmallow_geojson import MultiPointSchema
from marshmallow_geojson.object_type import MULTI_POINT

data = {
    "type": "MultiPoint",
    "coordinates": [
        [-105.01621, 39.57422],
        [-80.666513, 35.053994]
    ]
}
data_text = ujson.dumps(data)


class TestMultiPointSchema:
    def test_loads_schema(self):
        mp_schema = MultiPointSchema()
        mp_data = mp_schema.loads(data_text)

        coordinates = mp_data['coordinates']
        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item
            assert data['coordinates'][mpi_key] == [lon, lat]

        assert data['type'] == mp_data['type']

    def test_schema_type(self):
        mp_schema = MultiPointSchema()
        mp_data = mp_schema.loads(data_text)
        assert MULTI_POINT == mp_data['type']
