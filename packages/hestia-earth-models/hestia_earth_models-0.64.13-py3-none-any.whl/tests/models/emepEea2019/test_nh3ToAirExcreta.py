from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_emission

from hestia_earth.models.emepEea2019.nh3ToAirExcreta import MODEL, TERM_ID, run, _should_run

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
model_utils_path = f"hestia_earth.models.{MODEL}.utils"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"{class_path}.total_excreta_tan", return_value=None)
@patch(f"{class_path}._get_nh3_factor", return_value=None)
def test_should_run(mock_get_lookup_factor, mock_excreta, *args):
    cycle = {}

    # no excreta => no run
    mock_get_lookup_factor.return_value = 10
    should_run, *args = _should_run(cycle)
    assert not should_run

    # with excretaKgN => run
    cycle['inputs'] = [
        {
            'term': {
                '@id': 'excretaKgN',
                'termType': 'excreta',
                'units': 'kg N'
            },
            'value': [10]
        }
    ]
    mock_excreta.return_value = 10
    should_run, *args = _should_run(cycle)
    assert should_run is True


@patch(f"{model_utils_path}._new_emission", side_effect=fake_new_emission)
def test_run(*args):
    with open(f"{fixtures_folder}/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
