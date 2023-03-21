import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import MultiPointSchema
from marshmallow_geojson.object_type import MULTI_POINT


class TestMultiPointSchema:
    def test_loads_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data
        data_text = json.dumps(multi_point_dc)

        mp_schema = MultiPointSchema()
        mp_data = mp_schema.loads(data_text)

        coordinates = mp_data['coordinates']
        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item
            assert multi_point_dc['coordinates'][mpi_key] == [lon, lat]

        assert multi_point_dc['type'] == mp_data['type']

    def test_loads_many_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data
        data_text = json.dumps([multi_point_dc])

        mp_schema = MultiPointSchema(many=True)
        mp_data_list = mp_schema.loads(data_text)

        assert len(mp_data_list) == 1
        mp_data = mp_data_list[0]

        coordinates = mp_data['coordinates']
        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item
            assert multi_point_dc['coordinates'][mpi_key] == [lon, lat]

        assert multi_point_dc['type'] == mp_data['type']

    def test_load_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data

        mp_schema = MultiPointSchema()
        mp_data = mp_schema.load(multi_point_dc)

        coordinates = mp_data['coordinates']
        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item
            assert multi_point_dc['coordinates'][mpi_key] == [lon, lat]

        assert multi_point_dc['type'] == mp_data['type']

    def test_load_many_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data

        mp_schema = MultiPointSchema(many=True)
        mp_data_list = mp_schema.load([multi_point_dc])

        assert len(mp_data_list) == 1
        mp_data = mp_data_list[0]

        coordinates = mp_data['coordinates']
        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item
            assert multi_point_dc['coordinates'][mpi_key] == [lon, lat]

        assert multi_point_dc['type'] == mp_data['type']

    def test_dumps_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data
        data_text = json.dumps(multi_point_dc)

        mp_schema = MultiPointSchema()
        mp_data_text = mp_schema.dumps(multi_point_dc)

        assert json.loads(data_text) == json.loads(mp_data_text)

    def test_dumps_many_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data
        data_text = json.dumps([multi_point_dc])

        mp_schema = MultiPointSchema(many=True)
        mp_data_text = mp_schema.dumps([multi_point_dc])

        assert json.loads(data_text) == json.loads(mp_data_text)

    def test_dump_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data

        mp_schema = MultiPointSchema()
        mp_data = mp_schema.dump(multi_point_dc)

        coordinates = mp_data['coordinates']
        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item
            assert multi_point_dc['coordinates'][mpi_key] == [lon, lat]

        assert multi_point_dc['type'] == mp_data['type']

    def test_dump_many_schema(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data

        mp_schema = MultiPointSchema(many=True)
        mp_data_list = mp_schema.dump([multi_point_dc])

        assert len(mp_data_list) == 1
        mp_data = mp_data_list[0]

        coordinates = mp_data['coordinates']
        for mpi_key, mp_item in enumerate(coordinates):
            lon, lat = mp_item
            assert multi_point_dc['coordinates'][mpi_key] == [lon, lat]

        assert multi_point_dc['type'] == mp_data['type']

    def test_schema_type(self, get_multi_point_data):
        multi_point_dc = get_multi_point_data
        data_text = json.dumps(multi_point_dc)

        mp_schema = MultiPointSchema()
        mp_data = mp_schema.loads(data_text)
        assert MULTI_POINT == mp_data['type']

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        mp_schema = MultiPointSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid multi point type',
        ):
            mp_schema.loads(data_text)
