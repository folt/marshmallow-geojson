import json

import pytest
from marshmallow.exceptions import ValidationError

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

    def test_loads_many_schema(self, get_feature_data):
        feature_dc = get_feature_data
        data_text = json.dumps([feature_dc])

        f_schema = FeatureSchema(many=True)
        f_data_list = f_schema.loads(data_text)

        assert len(f_data_list) == 1
        f_data = f_data_list[0]

        geometry = f_data['geometry']
        assert geometry['type'] == f_data['geometry']['type']

        assert feature_dc['type'] == f_data['type']

    def test_load_schema(self, get_feature_data):
        feature_dc = get_feature_data

        f_schema = FeatureSchema()
        f_data = f_schema.load(feature_dc)

        geometry = f_data['geometry']
        assert geometry['type'] == f_data['geometry']['type']

        assert feature_dc['type'] == f_data['type']

    def test_load_many_schema(self, get_feature_data):
        feature_dc = get_feature_data

        f_schema = FeatureSchema(many=True)
        f_data_list = f_schema.load([feature_dc])

        assert len(f_data_list) == 1
        f_data = f_data_list[0]

        geometry = f_data['geometry']
        assert geometry['type'] == f_data['geometry']['type']

        assert feature_dc['type'] == f_data['type']

    def test_dumps_schema(self, get_feature_data):
        feature_dc = get_feature_data
        data_text = json.dumps(feature_dc)

        f_schema = FeatureSchema()
        f_data_text = f_schema.dumps(feature_dc)

        assert json.loads(data_text) == json.loads(f_data_text)

    def test_dumps_many_schema(self, get_feature_data):
        feature_dc = get_feature_data
        data_text = json.dumps([feature_dc])

        f_schema = FeatureSchema(many=True)
        f_data_text = f_schema.dumps([feature_dc])

        assert json.loads(data_text) == json.loads(f_data_text)

    def test_dump_schema(self, get_feature_data):
        feature_dc = get_feature_data

        f_schema = FeatureSchema()
        f_data = f_schema.dump(feature_dc)

        geometry = f_data['geometry']
        assert geometry['type'] == f_data['geometry']['type']

        assert feature_dc['type'] == f_data['type']

    def test_dump_many_schema(self, get_feature_data):
        feature_dc = get_feature_data

        f_schema = FeatureSchema(many=True)
        f_data_list = f_schema.dump([feature_dc])

        assert len(f_data_list) == 1
        f_data = f_data_list[0]

        geometry = f_data['geometry']
        assert geometry['type'] == f_data['geometry']['type']

        assert feature_dc['type'] == f_data['type']

    def test_schema_type(self, get_feature_data):
        feature_dc = get_feature_data
        data_text = json.dumps(feature_dc)

        f_schema = FeatureSchema()
        f_data = f_schema.loads(data_text)
        assert FEATURE == f_data['type']

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        f_schema = FeatureSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid feature type',
        ):
            f_schema.loads(data_text)
