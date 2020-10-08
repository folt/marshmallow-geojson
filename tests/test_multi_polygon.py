import ujson
from marshmallow_geojson import MultiPolygonSchema
from marshmallow_geojson.object_type import MULTI_POLYGON

data = {
    "type": "MultiPolygon",
    "coordinates": [
        [
            [
                [107, 7],
                [108, 7],
                [108, 8],
                [107, 8],
                [107, 7]
            ]
        ],
        [
            [
                [100, 0],
                [101, 0],
                [101, 1],
                [100, 1],
                [100, 0]
            ]
        ]
    ]
}
data_text = ujson.dumps(data)


class TestMultiPolygonSchema:
    def test_loads_schema(self):
        mp_schema = MultiPolygonSchema()
        mp_data = mp_schema.loads(data_text)

        coordinates = mp_data['coordinates']
        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate
                    assert data['coordinates'][mp_list_key][mp_item_key][
                               mpl_key] == [lon, lat]

        assert data['type'] == mp_data['type']

    def test_schema_type(self):
        mp_schema = MultiPolygonSchema()
        mp_data = mp_schema.loads(data_text)
        assert MULTI_POLYGON == mp_data['type']
