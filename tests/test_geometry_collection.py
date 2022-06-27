import json

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

    def test_schema_type(self, get_geometry_collection_data):
        geometry_collection_dc = get_geometry_collection_data
        data_text = json.dumps(geometry_collection_dc)

        gc_schema = GeometryCollectionSchema()
        gc_data = gc_schema.loads(data_text)
        assert GEOMETRY_COLLECTION == gc_data['type']
