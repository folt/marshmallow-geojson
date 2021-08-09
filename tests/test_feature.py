import json
from marshmallow_geojson import FeatureSchema
from marshmallow_geojson.object_type import FEATURE

data = {
    "type": "Feature",
    "geometry": {
        "type": "Polygon",
        "coordinates": [
            [
                [-80.724878, 35.265454],
                [-80.722646, 35.260338],
                [-80.720329, 35.260618],
                [-80.71681, 35.255361],
                [-80.704793, 35.268397],
                [-82.715179, 35.267696],
                [-80.721359, 35.267276],
                [-80.724878, 35.265454]
            ]
        ]
    },
    "properties": {}
}
data_text = json.dumps(data)


class TestFeatureSchema:
    def test_loads_schema(self):
        f_schema = FeatureSchema()
        f_data = f_schema.loads(data_text)

        geometry = f_data['geometry']
        assert geometry['type'] == f_data['geometry']['type']

        assert data['type'] == f_data['type']

    def test_schema_type(self):
        f_schema = FeatureSchema()
        f_data = f_schema.loads(data_text)
        assert FEATURE == f_data['type']
