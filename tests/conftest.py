import pytest

from marshmallow_geojson.examples import (
    GEOJSON_FEATURE_COLLECTION,
    GEOJSON_FEATURE_POLYGON,
    GEOJSON_GEOMETRY_COLLECTION,
    GEOJSON_LINE_STRING,
    GEOJSON_MULTI_LINE_STRING,
    GEOJSON_MULTI_POINT,
    GEOJSON_MULTI_POLYGON,
    GEOJSON_POINT,
    GEOJSON_POLYGON,
)


@pytest.fixture()
def get_feature_data():
    return GEOJSON_FEATURE_POLYGON.copy()


@pytest.fixture()
def get_feature_collection_data():
    return GEOJSON_FEATURE_COLLECTION.copy()


@pytest.fixture()
def get_point_data():
    return GEOJSON_POINT.copy()


@pytest.fixture()
def get_geometry_collection_data():
    return GEOJSON_GEOMETRY_COLLECTION.copy()


@pytest.fixture()
def get_line_string_data():
    return GEOJSON_LINE_STRING.copy()


@pytest.fixture()
def get_multi_line_string_data():
    return GEOJSON_MULTI_LINE_STRING.copy()


@pytest.fixture()
def get_multi_point_data():
    return GEOJSON_MULTI_POINT.copy()


@pytest.fixture()
def get_multi_polygon_data():
    return GEOJSON_MULTI_POLYGON.copy()


@pytest.fixture()
def get_polygon_data():
    return GEOJSON_POLYGON.copy()
