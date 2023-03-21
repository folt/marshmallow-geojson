import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import MultiPolygonSchema
from marshmallow_geojson.object_type import MULTI_POLYGON


class TestMultiPolygonSchema:
    def test_loads_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data
        data_text = json.dumps(multi_polygon_dc)

        mp_schema = MultiPolygonSchema()
        mp_data = mp_schema.loads(data_text)

        coordinates = mp_data['coordinates']
        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate
                    coord = multi_polygon_dc[
                        'coordinates'
                    ][mp_list_key][mp_item_key][mpl_key]
                    assert coord == [lon, lat]

        assert multi_polygon_dc['type'] == mp_data['type']

    def test_loads_many_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data
        data_text = json.dumps([multi_polygon_dc])

        mp_schema = MultiPolygonSchema(many=True)
        mp_data_list = mp_schema.loads(data_text)

        assert len(mp_data_list) == 1
        mp_data = mp_data_list[0]

        coordinates = mp_data['coordinates']
        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate
                    coord = multi_polygon_dc[
                        'coordinates'
                    ][mp_list_key][mp_item_key][mpl_key]
                    assert coord == [lon, lat]

        assert multi_polygon_dc['type'] == mp_data['type']

    def test_load_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data

        mp_schema = MultiPolygonSchema()
        mp_data = mp_schema.load(multi_polygon_dc)

        coordinates = mp_data['coordinates']
        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate
                    coord = multi_polygon_dc[
                        'coordinates'
                    ][mp_list_key][mp_item_key][mpl_key]
                    assert coord == [lon, lat]

        assert multi_polygon_dc['type'] == mp_data['type']

    def test_load_many_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data

        mp_schema = MultiPolygonSchema(many=True)
        mp_data_list = mp_schema.load([multi_polygon_dc])

        assert len(mp_data_list) == 1
        mp_data = mp_data_list[0]

        coordinates = mp_data['coordinates']
        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate
                    coord = multi_polygon_dc[
                        'coordinates'
                    ][mp_list_key][mp_item_key][mpl_key]
                    assert coord == [lon, lat]

        assert multi_polygon_dc['type'] == mp_data['type']

    def test_dumps_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data
        data_text = json.dumps(multi_polygon_dc)

        mp_schema = MultiPolygonSchema()
        mp_data_text = mp_schema.dumps(multi_polygon_dc)

        assert json.loads(data_text) == json.loads(mp_data_text)

    def test_dumps_many_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data
        data_text = json.dumps([multi_polygon_dc])

        mp_schema = MultiPolygonSchema(many=True)
        mp_data_text = mp_schema.dumps([multi_polygon_dc])

        assert json.loads(data_text) == json.loads(mp_data_text)

    def test_dump_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data

        mp_schema = MultiPolygonSchema()
        mp_data = mp_schema.dump(multi_polygon_dc)

        coordinates = mp_data['coordinates']
        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate
                    coord = multi_polygon_dc[
                        'coordinates'
                    ][mp_list_key][mp_item_key][mpl_key]
                    assert coord == [lon, lat]

        assert multi_polygon_dc['type'] == mp_data['type']

    def test_dump_many_schema(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data

        mp_schema = MultiPolygonSchema(many=True)
        mp_data_list = mp_schema.dump([multi_polygon_dc])

        assert len(mp_data_list) == 1
        mp_data = mp_data_list[0]

        coordinates = mp_data['coordinates']
        for mp_list_key, mp_list in enumerate(coordinates):
            for mp_item_key, mp_item in enumerate(mp_list):
                for mpl_key, mp_coordinate in enumerate(mp_item):
                    lon, lat = mp_coordinate
                    coord = multi_polygon_dc[
                        'coordinates'
                    ][mp_list_key][mp_item_key][mpl_key]
                    assert coord == [lon, lat]

        assert multi_polygon_dc['type'] == mp_data['type']

    def test_schema_type(self, get_multi_polygon_data):
        multi_polygon_dc = get_multi_polygon_data
        data_text = json.dumps(multi_polygon_dc)

        mp_schema = MultiPolygonSchema()
        mp_data = mp_schema.loads(data_text)
        assert MULTI_POLYGON == mp_data['type']

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        mp_schema = MultiPolygonSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid multi polygon type',
        ):
            mp_schema.loads(data_text)
