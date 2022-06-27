import json

import pytest
from marshmallow import ValidationError
from marshmallow.fields import List, Number

from marshmallow_geojson import PointSchema
from marshmallow_geojson.validate import Bbox


class BboxPointSchema(PointSchema):
    bbox = List(
        cls_or_instance=Number(
            required=True,
        ),
        required=True,
        validate=Bbox(
            min_lon=-180,
            max_lon=180,
            min_lat=-90,
            max_lat=90,
        ),
    )


class TestBboxSchema:
    def test_loads_schema(self, get_point_data):
        bbox_p_dc = get_point_data
        bbox_p_dc['bbox'] = [10, 10, 10, 10]
        data_text = json.dumps(bbox_p_dc)

        bbox_p_schema = BboxPointSchema()
        bbox_p_data = bbox_p_schema.loads(data_text)
        assert bbox_p_dc['bbox'] == bbox_p_data['bbox']

    def test_error_quantity(self, get_point_data):
        bbox_p_dc = get_point_data
        bbox_p_dc['bbox'] = [10, 10, 10]
        data_text = json.dumps(bbox_p_dc)

        bbox_p_schema = BboxPointSchema()

        with pytest.raises(
                ValidationError,
                match='2*n condition'
        ):
            bbox_p_schema.loads(data_text)

    def test_error_max_lon(self, get_point_data):
        bbox_p_dc = get_point_data
        bbox_p_dc['bbox'] = [200, 10, 10, 10]
        data_text = json.dumps(bbox_p_dc)

        bbox_p_schema = BboxPointSchema()

        with pytest.raises(
                ValidationError,
                match='Longitude must be between -180, 180.'
        ):
            bbox_p_schema.loads(data_text)

    def test_error_min_lon(self, get_point_data):
        bbox_p_dc = get_point_data
        bbox_p_dc['bbox'] = [-200, 10, 10, 10]
        data_text = json.dumps(bbox_p_dc)

        bbox_p_schema = BboxPointSchema()

        with pytest.raises(
                ValidationError,
                match='Longitude must be between -180, 180.'
        ):
            bbox_p_schema.loads(data_text)

    def test_error_max_lat(self, get_point_data):
        bbox_p_dc = get_point_data
        bbox_p_dc['bbox'] = [10, 100, 10, 10]
        data_text = json.dumps(bbox_p_dc)

        bbox_p_schema = BboxPointSchema()

        with pytest.raises(
                ValidationError,
                match='Latitude must be between -90, 90.'
        ):
            bbox_p_schema.loads(data_text)

    def test_error_min_lat(self, get_point_data):
        bbox_p_dc = get_point_data
        bbox_p_dc['bbox'] = [10, -100, 10, 10]
        data_text = json.dumps(bbox_p_dc)

        bbox_p_schema = BboxPointSchema()

        with pytest.raises(
                ValidationError,
                match='Latitude must be between -90, 90.'
        ):
            bbox_p_schema.loads(data_text)
