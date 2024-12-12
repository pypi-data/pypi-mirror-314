from unittest.mock import patch
import json
from tests.utils import fixtures_path, fake_new_indicator

from hestia_earth.models.blonkConsultants2016.landTransformationFromForest20YearAverageDuringCycle import (
    MODEL, TERM_ID, run, _should_run
)

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"{class_path}.land_occupation_per_kg", return_value=None)
@patch(f"{class_path}.get_emission_factor", return_value=None)
def test_should_run(mock_factor, mock_landOccupation):
    # with land occupation => no run
    mock_landOccupation.return_value = 10
    should_run, *args = _should_run({})
    assert not should_run

    # with emission factor => run
    mock_factor.return_value = 10
    should_run, *args = _should_run({})
    assert should_run is True


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run(*args):
    with open(f"{fixtures_folder}/impact-assessment.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected
