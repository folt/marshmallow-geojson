import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import PointSchema
from marshmallow_geojson.object_type import POINT


class TestPointSchema:
    def test_loads_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        p_schema = PointSchema()
        p_data = p_schema.loads(data_text)

        lon, lat = p_data['coordinates']
        assert point_dc['type'] == p_data['type']
        assert point_dc['coordinates'] == [lon, lat]

    def test_loads_many_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps([point_dc])

        p_schema = PointSchema(many=True)
        p_data_list = p_schema.loads(data_text)

        assert len(p_data_list) == 1
        p_data = p_data_list[0]

        lon, lat = p_data['coordinates']
        assert point_dc['type'] == p_data['type']
        assert point_dc['coordinates'] == [lon, lat]

    def test_load_schema(self, get_point_data):
        point_dc = get_point_data

        p_schema = PointSchema()
        p_data = p_schema.load(point_dc)

        lon, lat = p_data['coordinates']
        assert point_dc['type'] == p_data['type']
        assert point_dc['coordinates'] == [lon, lat]

    def test_load_many_schema(self, get_point_data):
        point_dc = get_point_data

        p_schema = PointSchema(many=True)
        p_data_list = p_schema.load([point_dc])

        assert len(p_data_list) == 1
        p_data = p_data_list[0]

        lon, lat = p_data['coordinates']
        assert point_dc['type'] == p_data['type']
        assert point_dc['coordinates'] == [lon, lat]

    def test_dumps_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        p_schema = PointSchema()
        p_data_text = p_schema.dumps(point_dc)

        assert json.loads(data_text) == json.loads(p_data_text)

    def test_dumps_many_schema(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps([point_dc])

        p_schema = PointSchema(many=True)
        p_data_text = p_schema.dumps([point_dc])

        assert json.loads(data_text) == json.loads(p_data_text)

    def test_schema_type(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        p_schema = PointSchema()
        p_data = p_schema.loads(data_text)
        assert POINT == p_data['type']

    def test_dump_schema(self, get_point_data):
        point_dc = get_point_data

        p_schema = PointSchema()
        p_data = p_schema.dump(point_dc)

        lon, lat = p_data['coordinates']
        assert point_dc['type'] == p_data['type']
        assert point_dc['coordinates'] == [lon, lat]

    def test_dump_many_schema(self, get_point_data):
        point_dc = get_point_data

        p_schema = PointSchema(many=True)
        p_data_list = p_schema.dump([point_dc])

        assert len(p_data_list) == 1
        p_data = p_data_list[0]

        lon, lat = p_data['coordinates']
        assert point_dc['type'] == p_data['type']
        assert point_dc['coordinates'] == [lon, lat]

    def test_schema_type_error(self, get_feature_data):
        feature_data_dc = get_feature_data
        data_text = json.dumps(feature_data_dc)

        p_schema = PointSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid point type',
        ):
            p_schema.loads(data_text)
