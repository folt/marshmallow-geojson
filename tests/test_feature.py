import json

from marshmallow_geojson import FeatureSchema
from marshmallow_geojson.object_type import FEATURE


class TestFeatureSchema:
    def test_loads_schema(self, get_feature_data):
        feature_dc = get_feature_data
        data_text = json.dumps(feature_dc)

        f_schema = FeatureSchema()
        f_data = f_schema.loads(data_text)

        geometry = f_data['geometry']
        assert geometry['type'] == f_data['geometry']['type']

        assert feature_dc['type'] == f_data['type']

    def test_schema_type(self, get_feature_data):
        feature_dc = get_feature_data
        data_text = json.dumps(feature_dc)

        f_schema = FeatureSchema()
        f_data = f_schema.loads(data_text)
        assert FEATURE == f_data['type']
