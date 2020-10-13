import ujson
from marshmallow_geojson import FeatureCollectionSchema
from marshmallow_geojson.object_type import FEATURE_COLLECTION

data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-80.870885, 35.215151]
            },
            "properties": {}
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-80.724878, 35.265454],
                        [-80.722646, 35.260338],
                        [-80.720329, 35.260618],
                        [-80.704793, 35.268397],
                        [-80.724878, 35.265454]
                    ]
                ]
            },
            "properties": {}
        }
    ]
}
data_text = ujson.dumps(data)


class TestFeatureCollectionSchema:
    def test_loads_schema(self):
        fc_schema = FeatureCollectionSchema()
        fc_data = fc_schema.loads(data_text)
        features = fc_data['features']

        for fc_key, fc_item in enumerate(features):
            assert fc_item['type'] == data['features'][fc_key]['type']

        assert data['type'] == fc_data['type']

    def test_schema_type(self):
        fc_schema = FeatureCollectionSchema()
        fc_data = fc_schema.loads(data_text)
        assert FEATURE_COLLECTION == fc_data['type']
