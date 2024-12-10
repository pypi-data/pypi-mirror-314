from unittest.mock import patch
import json

from tests.utils import fixtures_path, fake_new_indicator

from hestia_earth.models.edip2003.ozoneDepletionPotential import MODEL, TERM_ID, run

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run(*args):
    with open(f"{fixtures_folder}/impactassessment.jsonld", encoding='utf-8') as f:
        impactassessment = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(impactassessment)
    assert value == expected


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run_empty_input(*args):
    """
    Test with impact-assessment.jsonld that does NOT contain any "emissionsResourceUse".
    """

    with open(f"{fixtures_path}/impact_assessment/emissions/impact-assessment.jsonld", encoding='utf-8') as f:
        impactassessment = json.load(f)

    result = run(impactassessment)
    assert result['value'] == 0
