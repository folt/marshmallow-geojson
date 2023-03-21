import json

import pytest
from marshmallow.exceptions import ValidationError

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

    def test_loads_many_schema(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data
        data_text = json.dumps([feature_collection_dc])

        fc_schema = FeatureCollectionSchema(many=True)
        fc_data_list = fc_schema.loads(data_text)

        assert len(fc_data_list) == 1
        fc_data = fc_data_list[0]

        features = fc_data['features']

        for fc_key, fc_item in enumerate(features):
            data_item_type = feature_collection_dc['features'][fc_key]['type']
            assert fc_item['type'] == data_item_type

        assert feature_collection_dc['type'] == fc_data['type']

    def test_load_schema(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data

        fc_schema = FeatureCollectionSchema()
        fc_data = fc_schema.load(feature_collection_dc)

        features = fc_data['features']
        for fc_key, fc_item in enumerate(features):
            data_item_type = feature_collection_dc['features'][fc_key]['type']
            assert fc_item['type'] == data_item_type

        assert feature_collection_dc['type'] == fc_data['type']

    def test_load_many_schema(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data

        fc_schema = FeatureCollectionSchema(many=True)
        fc_data_list = fc_schema.load([feature_collection_dc])

        assert len(fc_data_list) == 1
        fc_data = fc_data_list[0]

        features = fc_data['features']
        for fc_key, fc_item in enumerate(features):
            data_item_type = feature_collection_dc['features'][fc_key]['type']
            assert fc_item['type'] == data_item_type

        assert feature_collection_dc['type'] == fc_data['type']

    def test_dumps_schema(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data
        data_text = json.dumps(feature_collection_dc)

        fc_schema = FeatureCollectionSchema()
        fc_data_text = fc_schema.dumps(feature_collection_dc)

        assert json.loads(data_text) == json.loads(fc_data_text)

    def test_dumps_many_schema(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data
        data_text = json.dumps([feature_collection_dc])

        fc_schema = FeatureCollectionSchema(many=True)
        fc_data_text = fc_schema.dumps([feature_collection_dc])

        assert json.loads(data_text) == json.loads(fc_data_text)

    def test_dump_schema(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data

        fc_schema = FeatureCollectionSchema()
        fc_data = fc_schema.dump(feature_collection_dc)

        features = fc_data['features']
        for fc_key, fc_item in enumerate(features):
            data_item_type = feature_collection_dc['features'][fc_key]['type']
            assert fc_item['type'] == data_item_type

        assert feature_collection_dc['type'] == fc_data['type']

    def test_dump_many_schema(self, get_feature_collection_data):
        feature_collection_dc = get_feature_collection_data

        fc_schema = FeatureCollectionSchema(many=True)
        fc_data_list = fc_schema.dump([feature_collection_dc])

        assert len(fc_data_list) == 1
        fc_data = fc_data_list[0]

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

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        fc_schema = FeatureCollectionSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid feature collection type',
        ):
            fc_schema.loads(data_text)
