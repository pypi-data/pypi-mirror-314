from unittest.mock import patch
import json
import pytest

from tests.utils import fixtures_path, fake_new_measurement

from hestia_earth.models.site.soilMeasurement import (
    MODEL,
    MODEL_KEY,
    _get_overlap,
    _harmonise_measurements,
    _should_run, run
)

class_path = f"hestia_earth.models.{MODEL}.{MODEL_KEY}"
fixtures_folder = f"{fixtures_path}/site/soilMeasurement"


@pytest.mark.parametrize(
    "data,expected",
    [
        ((1, 10, 2, 150), 8),
        ((1, 10, 5, 15), 5),
        ((1, 10, 10, 15), 0),
        ((10, 10, 0, 150), 0),
        ((150, 155, 1, 150), 0),
        ((20, 40, 0, 30), 10),
        ((0, 20, 0, 50), 20),
        ((20, 60, 0, 50), 30),
        ((10, 20, 40, 50), 0),
        ((10, 20, 19, 50), 1),
    ]
)
def test_get_overlap(data, expected):
    result = _get_overlap(
        data[0], data[1], data[2], data[3]
    )
    assert result == expected


@pytest.mark.parametrize(
    "measurements_list,returns_dict,expected_value",
    [
        (
            [
                {"value": [7.5], "depthUpper": 0, "depthLower": 20},
                {"value": [6], "depthUpper": 20, "depthLower": 40},
            ],
            {"depthUpper": 0, "depthLower": 30},
            7
        ),
        (
            [
                {"value": [7.5], "depthUpper": 0, "depthLower": 20},
                {"value": [6], "depthUpper": 20, "depthLower": 40},
            ],
            {"depthUpper": 0, "depthLower": 50},
            6.75
        ),
    ]
)
def test_harmonise_measurements(measurements_list, returns_dict, expected_value):
    actual_value = _harmonise_measurements(
        measurements_list=measurements_list,
        standard_depth_upper=returns_dict["depthUpper"],
        standard_depth_lower=returns_dict["depthLower"],
    )
    assert actual_value == expected_value


@pytest.mark.parametrize(
    "test_name,site,expected_should_run",
    [
        (
            "no measurement => no run",
            {"measurements": []},
            False
        ),
        (
            "missing dates => run",
            {
                "measurements": [
                    {
                        "term": {"@id": "clayContent"},
                        "depthUpper": 0,
                        "depthLower": 20,
                        "value": [0]
                    }
                ]
            },
            True
        ),
        (
            "no depthUpper => no run",
            {
                "measurements": [
                    {
                        "term": {"@id": "clayContent"},
                        "dates": ["2022-01-02"],
                        "depthLower": 20,
                        "value": [0]
                    }
                ]
            },
            False
        ),
        (
            "missing value => not run",
            {
                "measurements": [
                    {
                        "term": {"@id": "clayContent"},
                        "dates": ["2022-01-02"],
                        "depthUpper": 0,
                        "depthLower": 20
                    }
                ]
            },
            False
        ),
        (
            "all fields => run",
            {
                "measurements": [
                    {
                        "term": {"@id": "clayContent"},
                        "dates": ["2022-01-02"],
                        "depthUpper": 0,
                        "depthLower": 20,
                        "value": [0]
                    }
                ]
            },
            True
        )
    ]
)
def test_should_run(test_name, site, expected_should_run):
    should_run, *args = _should_run(site)
    assert should_run == expected_should_run, test_name


@pytest.mark.parametrize(
    "test_name",
    [
        "missing-depth",
        "missing-value",
        "simple-soilPh",
        "clayContent",
        "non-unique-measurements",
        "arrays",
        "standard-intervals"
    ]
)
@patch(f"{class_path}._new_measurement", side_effect=fake_new_measurement)
def test_run(mock_new_measurement, test_name):
    with open(f"{fixtures_folder}/{test_name}/site.jsonld", encoding='utf-8') as f:
        site = json.load(f)

    with open(f"{fixtures_folder}/{test_name}/result.jsonld", encoding='utf-8') as f:
        result = json.load(f)

    value = run(site)
    assert value == result
