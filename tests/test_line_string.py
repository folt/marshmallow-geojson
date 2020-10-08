import ujson
from marshmallow_geojson import LineStringSchema
from marshmallow_geojson.object_type import LINE_STRING

data = {
    "type": "LineString",
    "coordinates": [
        [-99.113159, 38.869651],
        [-99.0802, 38.85682],
        [-98.822021, 38.85682],
        [-98.448486, 38.848264]
    ]
}
data_text = ujson.dumps(data)


class TestLineStringSchema:
    def test_loads_schema(self):
        ls_schema = LineStringSchema()
        ls_data = ls_schema.loads(data_text)

        coordinates = ls_data['coordinates']
        for lsi_key, ls_item in enumerate(coordinates):
            lon, lat = ls_item
            assert data['coordinates'][lsi_key] == [lon, lat]

        assert data['type'] == ls_data['type']

    def test_schema_type(self):
        ls_schema = LineStringSchema()
        ls_data = ls_schema.loads(data_text)
        assert LINE_STRING == ls_data['type']
