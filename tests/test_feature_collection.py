import json

from marshmallow_geojson import FeatureCollectionSchema
from marshmallow_geojson.object_type import FEATURE_COLLECTION


class TestFeatureCollectionSchema:
    def test_loads_schema(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data
        data_text = json.dumps(feature_collection_dc)

        fc_schema = FeatureCollectionSchema()
        fc_data = fc_schema.loads(data_text)
        features = fc_data['features']

        for fc_key, fc_item in enumerate(features):
            data_item_type = feature_collection_dc['features'][fc_key]['type']
            assert fc_item['type'] == data_item_type

        assert feature_collection_dc['type'] == fc_data['type']

    def test_schema_type(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data
        data_text = json.dumps(feature_collection_dc)

        fc_schema = FeatureCollectionSchema()
        fc_data = fc_schema.loads(data_text)
        assert FEATURE_COLLECTION == fc_data['type']
