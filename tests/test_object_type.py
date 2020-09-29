from marshmallow_geojson import (
    object_type,
)


class TestFormatStringType:
    def test_format_string_for_point(self):
        assert object_type.POINT == 'Point'

    def test_format_string_for_multi_point(self):
        assert object_type.MULTI_POINT == 'MultiPoint'

    def test_format_string_for_line_string(self):
        assert object_type.LINE_STRING == 'LineString'

    def test_format_string_for_multi_line_string(self):
        assert object_type.MULTI_LINE_STRING == 'MultiLineString'

    def test_format_string_for_polygon(self):
        assert object_type.POLYGON == 'Polygon'

    def test_format_string_for_multi_polygon(self):
        assert object_type.MULTI_POLYGON == 'MultiPolygon'

    def test_format_string_for_geometry_collection(self):
        assert object_type.GEOMETRY_COLLECTION == 'GeometryCollection'

    def test_format_string_for_feature(self):
        assert object_type.FEATURE == 'Feature'

    def test_format_string_for_feature_collection(self):
        assert object_type.FEATURE_COLLECTION == 'FeatureCollection'


class TestGeometryType:
    def test_geometry_type_value_for_point(self):
        value = object_type.GeometryType.point.value
        assert value == object_type.POINT

    def test_geometry_type_value_for_multi_point(self):
        value = object_type.GeometryType.multi_point.value
        assert value == object_type.MULTI_POINT

    def test_geometry_type_value_for_line_string(self):
        value = object_type.GeometryType.line_string.value
        assert value == object_type.LINE_STRING

    def test_geometry_type_value_for_multi_line_string(self):
        value = object_type.GeometryType.multi_line_string.value
        assert value == object_type.MULTI_LINE_STRING

    def test_geometry_type_value_for_polygon(self):
        value = object_type.GeometryType.polygon.value
        assert value == object_type.POLYGON

    def test_geometry_type_value_for_multi_polygon(self):
        value = object_type.GeometryType.multi_polygon.value
        assert value == object_type.MULTI_POLYGON

    def test_geometry_type_value_for_geometry_collection(self):
        value = object_type.GeometryType.geometry_collection.value
        assert value == object_type.GEOMETRY_COLLECTION

    def test_geometry_type_len(self):
        assert 7 == len([item.value for item in object_type.GeometryType])


class TestGeoJSONType:
    def test_geo_json_type_value_for_point(self):
        value = object_type.GeoJSONType.point.value
        assert value == object_type.POINT

    def test_geo_json_type_value_for_multi_point(self):
        value = object_type.GeoJSONType.multi_point.value
        assert value == object_type.MULTI_POINT

    def test_geo_json_type_value_for_line_string(self):
        value = object_type.GeoJSONType.line_string.value
        assert value == object_type.LINE_STRING

    def test_geo_json_type_value_for_multi_line_string(self):
        value = object_type.GeoJSONType.multi_line_string.value
        assert value == object_type.MULTI_LINE_STRING

    def test_geo_json_type_value_for_polygon(self):
        value = object_type.GeoJSONType.polygon.value
        assert value == object_type.POLYGON

    def test_geo_json_type_value_for_multi_polygon(self):
        value = object_type.GeoJSONType.multi_polygon.value
        assert value == object_type.MULTI_POLYGON

    def test_geo_json_type_value_for_geometry_collection(self):
        value = object_type.GeoJSONType.geometry_collection.value
        assert value == object_type.GEOMETRY_COLLECTION

    def test_geo_json_type_value_for_feature(self):
        value = object_type.GeoJSONType.feature.value
        assert value == object_type.FEATURE

    def test_geo_json_type_value_for_feature_collection(self):
        value = object_type.GeoJSONType.feature_collection.value
        assert value == object_type.FEATURE_COLLECTION

    def test_geometry_type_len(self):
        assert 9 == len([item.value for item in object_type.GeoJSONType])
