import json
from unittest.mock import patch

from pytest import mark

from hestia_earth.models.environmentalFootprintV3.soilQualityIndexLandTransformation import MODEL, TERM_ID, run, \
    _should_run
from tests.utils import fixtures_path, fake_new_indicator

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


def fake_rounded_indicator(value: float):
    indicator = fake_new_indicator(TERM_ID, MODEL)
    indicator['value'] = round(value, 7)
    return indicator


crop_land = {"@id": "cropland", "termType": "landCover"}
sea_land_cover = {"@id": "seaOrOcean", "termType": "landCover"}
forest = {"@id": "forest", "termType": "landCover"}

wrong_indicator = {"term": {"@id": "NOT_VALID_INDICATOR_ID", "termType": "resourceUse", "units": "m2 / year"},
                   "value": 0.5, "landCover": crop_land}

indicator_no_land_cover = {
    "term": {"@id": "landTransformationFromForest20YearAverageInputsProduction", "termType": "resourceUse",
             "units": "m2 / year"},
    "value": 0.5}

indicator_no_unit = {
    "term": {"@id": "landTransformationFromForest20YearAverageInputsProduction", "termType": "resourceUse"},
    "value": 0.5, "landCover": crop_land}

indicator_wrong_unit = {
    "term": {"@id": "landTransformationFromForest20YearAverageInputsProduction", "termType": "resourceUse",
             "units": "ha*day"}, "value": 0.5,
    "landCover": crop_land}

indicator_bad_area_value = {
    "term": {"@id": "landTransformationFromForest20YearAverageInputsProduction", "termType": "resourceUse",
             "units": "m2 / year"}, "value": -10,
    "landCover": crop_land}

inputs_production_indicator_from_forest_to_no_cf = {
    "term": {"@id": "landTransformationFromForest20YearAverageInputsProduction", "termType": "resourceUse",
             "units": "m2 / year"}, "value": 0.5,
    "landCover": sea_land_cover}

good_inputs_production_indicator_from_forest_to_cropland = {
    "term": {"@id": "landTransformationFromForest20YearAverageInputsProduction", "termType": "resourceUse",
             "units": "m2 / year"}, "value": 0.5,
    "landCover": crop_land}

good_inputs_production_indicator_from_forest_to_forest = {
    "term": {"@id": "landTransformationFromForest20YearAverageInputsProduction", "termType": "resourceUse",
             "units": "m2 / year"}, "value": 0.5,
    "landCover": forest}

good_during_cycle_indicator_from_forest_to_cropland = {
    "term": {"@id": "landTransformationFromForest20YearAverageDuringCycle", "termType": "resourceUse",
             "units": "m2 / year"}, "value": 0.5,
    "landCover": crop_land}

good_during_cycle_indicator_from_forest_to_forest = {
    "term": {"@id": "landTransformationFromForest20YearAverageDuringCycle", "termType": "resourceUse",
             "units": "m2 / year"}, "value": 0.5,
    "landCover": forest}


@mark.parametrize(
    "resources, expected, num_inputs",
    [
        ([], True, 0),
        ([wrong_indicator], True, 0),
        ([indicator_no_land_cover], False, 0),
        ([indicator_no_unit], False, 0),
        ([indicator_wrong_unit], False, 0),
        ([indicator_bad_area_value], False, 0),
        ([good_during_cycle_indicator_from_forest_to_cropland], True, 1),
        ([good_during_cycle_indicator_from_forest_to_forest], True, 1),
        ([good_inputs_production_indicator_from_forest_to_cropland], True, 1),
        ([good_inputs_production_indicator_from_forest_to_forest], True, 1),
        ([inputs_production_indicator_from_forest_to_no_cf], True, 0),  # todo check
        ([good_inputs_production_indicator_from_forest_to_cropland,
          good_during_cycle_indicator_from_forest_to_cropland], True, 2)
    ],
    ids=["No emissionsResourceUse => run, 0 dict",
         "Wrong indicator termid => run, 0 dict",
         "Indicator no landcover terms => no run",
         "Missing unit => no run",
         "Wrong unit => no run",
         "Bad m2 / year value => no run",
         "One good during cycle transformation => run, 1 dict",
         "One 0 during cycle transformation => run, 1 dict",
         "One good inputs production transformation => run, 1 dict",
         "One 0 inputs production transformation => run, 1 dict",
         "One good from transformation and One with no CF (ocean) => run, 2 dict",  # todo
         "Multiple good indicators => run, 2 dict",
         ]
)
@patch(f"{class_path}.get_land_cover_terms", return_value=['cropland', 'seaOrOcean', 'forest'])
def test_should_run(mock_download, resources, expected, num_inputs):
    with open(f"{fixtures_folder}/multipleTransformations/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    impact['emissionsResourceUse'] = resources

    should_run, resources_with_cf = _should_run(impact)
    assert should_run is expected
    assert len(resources_with_cf) == num_inputs


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run(*args):
    with open(f"{fixtures_folder}/multipleTransformations/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    with open(f"{fixtures_folder}/multipleTransformations/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(impact)
    assert value == expected


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run_italy(*args):
    with open(f"{fixtures_folder}/Italy/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    with open(f"{fixtures_folder}/Italy/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(impact)
    assert value == expected


@mark.parametrize(
    "added_data",
    [
        {"country": {}},
        {"country": {"@id": "region-europe", "@type": "Term", "name": "Europe"}},
    ],
    ids=["No country/region => default to region world",
         "region-europe not in the lookup file => default to region world"]
)
@patch(f"{class_path}._indicator", side_effect=fake_rounded_indicator)
def test_run_with_country_fallback(mocked_indicator, added_data):
    """
    When given valid sub-region or country not in the lookup file, default to country 'region-world' with value 574.56
    """

    with open(f"{fixtures_folder}/multipleTransformations/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    impact = impact | added_data

    value = run(impact)
    assert value['value'] == 574.56


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run_no_transformation(*args):
    """
    Impact assessment with no transformations should return a indicator of 0
    """
    with open(f"{fixtures_folder}/multipleTransformations/impact-assessment.jsonld", encoding='utf-8') as f:
        impact = json.load(f)

    impact['emissionsResourceUse'] = []

    value = run(impact)

    assert value['value'] == 0
