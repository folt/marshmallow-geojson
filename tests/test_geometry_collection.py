import json

import pytest
from marshmallow.exceptions import ValidationError

from marshmallow_geojson import GeometryCollectionSchema
from marshmallow_geojson.object_type import GEOMETRY_COLLECTION


class TestGeometryCollectionSchema:
    def test_loads_schema(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data
        data_text = json.dumps(geometry_collection_dc)

        gc_schema = GeometryCollectionSchema()
        gc_data = gc_schema.loads(data_text)

        geometries = gc_data['geometries']

        for g_k, g_i in enumerate(geometries):
            data_item_type = geometry_collection_dc['geometries'][g_k]['type']
            assert data_item_type == g_i['type']

        assert geometry_collection_dc['type'] == gc_data['type']

    def test_loads_many_schema(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data
        data_text = json.dumps([geometry_collection_dc])

        gc_schema = GeometryCollectionSchema(many=True)
        gc_data_list = gc_schema.loads(data_text)

        assert len(gc_data_list) == 1
        gc_data = gc_data_list[0]

        geometries = gc_data['geometries']

        for g_k, g_i in enumerate(geometries):
            data_item_type = geometry_collection_dc['geometries'][g_k]['type']
            assert data_item_type == g_i['type']

        assert geometry_collection_dc['type'] == gc_data['type']

    def test_load_schema(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data

        gc_schema = GeometryCollectionSchema()
        gc_data = gc_schema.load(geometry_collection_dc)

        geometries = gc_data['geometries']

        for g_k, g_i in enumerate(geometries):
            data_item_type = geometry_collection_dc['geometries'][g_k]['type']
            assert data_item_type == g_i['type']

        assert geometry_collection_dc['type'] == gc_data['type']

    def test_load_many_schema(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data

        gc_schema = GeometryCollectionSchema(many=True)
        gc_data_list = gc_schema.load([geometry_collection_dc])

        assert len(gc_data_list) == 1
        gc_data = gc_data_list[0]

        geometries = gc_data['geometries']

        for g_k, g_i in enumerate(geometries):
            data_item_type = geometry_collection_dc['geometries'][g_k]['type']
            assert data_item_type == g_i['type']

        assert geometry_collection_dc['type'] == gc_data['type']

    def test_dumps_schema(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data
        data_text = json.dumps(geometry_collection_dc)

        gc_schema = GeometryCollectionSchema()
        gc_data_text = gc_schema.dumps(geometry_collection_dc)

        assert json.loads(data_text) == json.loads(gc_data_text)

    def test_dumps_many_schema(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data
        data_text = json.dumps([geometry_collection_dc])

        gc_schema = GeometryCollectionSchema(many=True)
        gc_data_text = gc_schema.dumps([geometry_collection_dc])

        assert json.loads(data_text) == json.loads(gc_data_text)

    def test_dump_schema(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data

        gc_schema = GeometryCollectionSchema()
        gc_data = gc_schema.dump(geometry_collection_dc)

        geometries = gc_data['geometries']

        for g_k, g_i in enumerate(geometries):
            data_item_type = geometry_collection_dc['geometries'][g_k]['type']
            assert data_item_type == g_i['type']

        assert geometry_collection_dc['type'] == gc_data['type']

    def test_dump_many_schema(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data

        gc_schema = GeometryCollectionSchema(many=True)
        gc_data_list = gc_schema.dump([geometry_collection_dc])

        assert len(gc_data_list) == 1
        gc_data = gc_data_list[0]

        geometries = gc_data['geometries']

        for g_k, g_i in enumerate(geometries):
            data_item_type = geometry_collection_dc['geometries'][g_k]['type']
            assert data_item_type == g_i['type']

        assert geometry_collection_dc['type'] == gc_data['type']

    def test_schema_type(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data
        data_text = json.dumps(geometry_collection_dc)

        gc_schema = GeometryCollectionSchema()
        gc_data = gc_schema.loads(data_text)
        assert GEOMETRY_COLLECTION == gc_data['type']

    def test_schema_type_error(self, get_point_data):
        point_dc = get_point_data
        data_text = json.dumps(point_dc)

        gc_schema = GeometryCollectionSchema()
        with pytest.raises(
            ValidationError,
            match='Invalid geometry collection type',
        ):
            gc_schema.loads(data_text)
