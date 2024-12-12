import json
from unittest.mock import Mock, patch
import pytest
from hestia_earth.schema import SiteSiteType

from tests.utils import fixtures_path, fake_new_management
from hestia_earth.models.site.management import MODEL, MODEL_KEY, run

class_path = f"hestia_earth.models.{MODEL}.{MODEL_KEY}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{MODEL_KEY}"

_LAND_COVER_TERM_BY_SITE_TYPE = {
    SiteSiteType.ANIMAL_HOUSING.value: "animalHousing",
    SiteSiteType.CROPLAND.value: "cropland"
}


@pytest.mark.parametrize(
    "test_name,fixture_path",
    [
        ("Products and practices", f"{fixtures_folder}"),
        ("Example 1", f"{fixtures_folder}/inputs/example1"),
        ("Example 2", f"{fixtures_folder}/inputs/example2"),
        ("Example 3", f"{fixtures_folder}/inputs/example3"),
        ("Example 4", f"{fixtures_folder}/inputs/example4"),
        ("Condense Nodes", f"{fixtures_folder}/inputs/condense_nodes"),
        # Expected:
        #   - appleTree (81) x 3 condenses 2020-03-01 to 2021-02-15
        #   - animalManureUsed (true) x 2 condenses 2001-04-01 to 2001-12-31
        #   - treeNutTree, lebbekTree (82) does not condense [different terms]
        #   - organicFertiliserUsed (true|false) does not condense [different values]
        #   - glassOrHighAccessibleCover (83) does not condense [different date ranges (overlapping)]
        #   - durianTree (84) does not condense [different date ranges (disjoint)]
        #   - irrigatedSurfaceIrrigationContinuouslyFlooded (85) does not condense ["%" units]
        #   - sassafrasTree (86) x 2 condenses 2001-01-01 to 2004-12-31
        #   - bananaPlant (87) does not condense [non-consecutive years]
        #   - durianTree (89) does not condense [dates overwritten See 808]
        ("Site Type", f"{fixtures_folder}/inputs/site_type"),
        ("Multiple products but only 1 with landCover id", f"{fixtures_folder}/multiple-products"),
    ]
)
@patch(
    f"{class_path}.get_landCover_term_id_from_site_type",
    side_effect=lambda site_type: _LAND_COVER_TERM_BY_SITE_TYPE[site_type]
)
@patch(f"{class_path}._new_management", side_effect=fake_new_management)
@patch(f"{class_path}.related_cycles")
def test_run(
        mock_related_cycles: Mock,
        mock_new_management: Mock,
        mock_land_cover_lookup: Mock,
        test_name: str,
        fixture_path: str
):
    with open(f"{fixture_path}/cycles.jsonld", encoding='utf-8') as f:
        cycles = json.load(f)
    mock_related_cycles.return_value = cycles

    try:
        with open(f"{fixture_path}/site.jsonld", encoding='utf-8') as f:
            site = json.load(f)
    except FileNotFoundError:
        with open(f"{fixtures_folder}/site.jsonld", encoding='utf-8') as f:
            site = json.load(f)

    with open(f"{fixture_path}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    result = run(site)
    assert result == expected, test_name
