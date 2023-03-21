import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import PolygonSchema
from marshmallow_geojson.object_type import POLYGON


class TestPolygonSchema:
    def test_loads_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data
        data_text = json.dumps(polygon_dc)

        p_schema = PolygonSchema()
        p_data = p_schema.loads(data_text)

        coordinates = p_data['coordinates']
        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate
                assert polygon_dc['coordinates'][pi_key][pl_key] == [lon, lat]

        assert polygon_dc['type'] == p_data['type']

    def test_loads_many_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data
        data_text = json.dumps([polygon_dc])

        p_schema = PolygonSchema(many=True)
        p_data_list = p_schema.loads(data_text)

        assert len(p_data_list) == 1
        p_data = p_data_list[0]

        coordinates = p_data['coordinates']
        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate
                assert polygon_dc['coordinates'][pi_key][pl_key] == [lon, lat]

        assert polygon_dc['type'] == p_data['type']

    def test_load_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data

        p_schema = PolygonSchema()
        p_data = p_schema.load(polygon_dc)

        coordinates = p_data['coordinates']
        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate
                assert polygon_dc['coordinates'][pi_key][pl_key] == [lon, lat]

    def test_load_many_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data

        p_schema = PolygonSchema(many=True)
        p_data_list = p_schema.load([polygon_dc])

        assert len(p_data_list) == 1
        p_data = p_data_list[0]

        coordinates = p_data['coordinates']
        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate
                assert polygon_dc['coordinates'][pi_key][pl_key] == [lon, lat]

    def test_dumps_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data
        data_text = json.dumps(polygon_dc)

        p_schema = PolygonSchema()
        p_data_text = p_schema.dumps(polygon_dc)

        assert json.loads(data_text) == json.loads(p_data_text)

    def test_dumps_many_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data
        data_text = json.dumps([polygon_dc])

        p_schema = PolygonSchema(many=True)
        p_data_text = p_schema.dumps([polygon_dc])

        assert json.loads(data_text) == json.loads(p_data_text)

    def test_dump_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data

        p_schema = PolygonSchema()
        p_data = p_schema.dump(polygon_dc)

        coordinates = p_data['coordinates']
        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate
                assert polygon_dc['coordinates'][pi_key][pl_key] == [lon, lat]

        assert polygon_dc['type'] == p_data['type']

    def test_dump_many_schema(self, get_polygon_data):
        polygon_dc = get_polygon_data

        p_schema = PolygonSchema(many=True)
        p_data_list = p_schema.dump([polygon_dc])

        assert len(p_data_list) == 1
        p_data = p_data_list[0]

        coordinates = p_data['coordinates']
        for pi_key, p_item in enumerate(coordinates):
            for pl_key, p_coordinate in enumerate(p_item):
                lon, lat = p_coordinate
                assert polygon_dc['coordinates'][pi_key][pl_key] == [lon, lat]

        assert polygon_dc['type'] == p_data['type']

    def test_schema_type(self, get_polygon_data):
        polygon_dc = get_polygon_data
        data_text = json.dumps(polygon_dc)

        p_schema = PolygonSchema()
        p_data = p_schema.loads(data_text)
        assert POLYGON == p_data['type']

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        p_schema = PolygonSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid polygon type',
        ):
            p_schema.loads(data_text)
