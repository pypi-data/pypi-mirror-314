from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_indicator

from hestia_earth.models.hyde32.landTransformationFromCropland100YearAverageDuringCycle import TERM_ID, run

class_path = f"hestia_earth.models.hyde32.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/hyde32/{TERM_ID}"


@patch('hestia_earth.models.hyde32.utils.get_land_cover_term_id', return_value='cropland')
@patch('hestia_earth.models.hyde32.utils._new_indicator', side_effect=fake_new_indicator)
def test_run(*args):
    with open(f"{fixtures_folder}/impact-assessment.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
