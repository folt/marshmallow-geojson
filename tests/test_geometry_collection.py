import json

from marshmallow_geojson import GeometryCollectionSchema
from marshmallow_geojson.object_type import GEOMETRY_COLLECTION

data = {
    "type": "GeometryCollection",
    "geometries": [
        {
            "type": "Point",
            "coordinates": [-80.660805, 35.049392]
        },
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [-80.664582, 35.044965],
                    [-80.663874, 35.04428],
                    [-80.662586, 35.04558],
                    [-80.663444, 35.046036],
                    [-80.664582, 35.044965]
                ]
            ]
        },
        {
            "type": "LineString",
            "coordinates": [
                [-80.662372, 35.059509],
                [-80.662693, 35.059263],
                [-80.662844, 35.05893]
            ]
        }
    ]
}
data_text = json.dumps(data)


class TestGeometryCollectionSchema:
    def test_loads_schema(self):
        gc_schema = GeometryCollectionSchema()
        gc_data = gc_schema.loads(data_text)

        geometries = gc_data['geometries']

        for g_k, g_i in enumerate(geometries):
            assert data['geometries'][g_k]['type'] == g_i['type']

        assert data['type'] == gc_data['type']

    def test_schema_type(self):
        gc_schema = GeometryCollectionSchema()
        gc_data = gc_schema.loads(data_text)
        assert GEOMETRY_COLLECTION == gc_data['type']
