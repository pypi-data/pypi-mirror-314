from unittest.mock import patch

import numpy

from hestia_earth.models.faostat2018.utils import (get_sum_of_columns, MODEL, get_land_ratio,
                                                   get_change_in_harvested_area_for_crop)
from tests.utils import fixtures_path

CLASS_PATH = f"hestia_earth.models.{MODEL}.utils"
fixtures_folder = f"{fixtures_path}/{MODEL}/utils"


def _afg_download_fixture():
    with open(f"{fixtures_folder}/gadm-afg.csv") as f:
        afg_lookup = numpy.recfromcsv(
            fname=f,
            missing_values="",
            filling_values="",
            delimiter=",",
            encoding="utf-8"
        )
    return afg_lookup


def test_get_sum_of_columns():
    result = get_sum_of_columns(
        lookup=_afg_download_fixture(),
        country="GADM-AFG",
        year=1975,
        columns_list=["Arable land", "Permanent crops"]
    )
    assert result == 8050.3


def test_check_sums_for_columns():
    """
    Check that the values of Arable and Permanent add up to Cropland, at least for AFG
    """
    for year in range(1961, 2021):
        sum_arab_perm = get_sum_of_columns(
            lookup=_afg_download_fixture(),
            country="GADM-AFG",
            year=year,
            columns_list=["Arable land", "Permanent crops"]
        )

        cropland_value = get_sum_of_columns(
            lookup=_afg_download_fixture(),
            country="GADM-AFG",
            year=year,
            columns_list=["Cropland"]
        )
        assert sum_arab_perm == cropland_value


@patch(f"{CLASS_PATH}.download_lookup")
def test_get_land_ratio(mock_lookup):
    mock_lookup.return_value = _afg_download_fixture()
    result = get_land_ratio(
        country="GADM-AFG",
        start_year=1990,
        end_year=2010,
        first_column="Forest land",
        second_column="Cropland"
    )

    assert result == (-123.0, 0.0, -123.0)


def test_get_harvested_area_for_crop():
    result = get_change_in_harvested_area_for_crop(
        country_id="GADM-AFG",
        start_year=1990,
        end_year=1992,
        crop_name="Wheat"
    )
    assert result == 30000.0

    result = get_change_in_harvested_area_for_crop(
        country_id="GADM-AFG",
        start_year=2019,
        crop_name="Wheat"
    )
    assert result == 2334000
