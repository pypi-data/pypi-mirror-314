from functools import reduce
import json
from os.path import isfile
from pytest import mark
from unittest.mock import patch

from hestia_earth.models.ipcc2019.co2ToAirAboveGroundBiomassStockChange import MODEL, run

from tests.utils import fake_new_emission, fixtures_path, order_list

class_path = f"hestia_earth.models.{MODEL}.co2ToAirAboveGroundBiomassStockChange"
utils_path = f"hestia_earth.models.{MODEL}.co2ToAirCarbonStockChange_utils"
fixtures_folder = f"{fixtures_path}/{MODEL}/co2ToAirAboveGroundBiomassStockChange"

RUN_SCENARIOS = [
    ("no-overlapping-cycles", 3),
    ("overlapping-cycles", 4),
    ("complex-overlapping-cycles", 5),
    ("missing-measurement-dates", 3),
    ("no-biomass-measurements", 1),               # Closes issue #700
    ("non-consecutive-biomass-measurements", 1),  # Closes issue #827
    ("multiple-method-classifications", 5),       # Closes issue #764
    ("non-soil-based-gohac-system", 3),           # Closes issue #848
    ("soil-based-gohac-system", 3),               # Closes issue #848
    ("with-gapfilled-start-date-end-date", 1)     # Closes issue #972
]
"""List of (subfolder: str, num_cycles: int)."""


def _load_fixture(path: str, default=None):
    if isfile(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


RUN_PARAMS = reduce(
    lambda params, scenario: params + [(scenario[0], scenario[1], i) for i in range(scenario[1])],
    RUN_SCENARIOS,
    list()
)
"""List of (subfolder: str, num_cycles: int, cycle_index: int)."""

RUN_IDS = [f"{param[0]}, cycle{param[2]}" for param in RUN_PARAMS]


@mark.parametrize("subfolder, num_cycles, cycle_index", RUN_PARAMS, ids=RUN_IDS)
@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
@patch(f"{utils_path}.related_cycles")
@patch(f"{utils_path}._get_site")  # TODO: rationalise order of patches
def test_run(_get_site_mock, related_cycles_mock, _new_emission_mock, subfolder, num_cycles, cycle_index):
    """
    Test `run` function for each cycle in each scenario.
    """
    site = _load_fixture(f"{fixtures_folder}/{subfolder}/site.jsonld")
    cycle = _load_fixture(f"{fixtures_folder}/{subfolder}/cycle{cycle_index}.jsonld")
    expected = _load_fixture(f"{fixtures_folder}/{subfolder}/result{cycle_index}.jsonld", default=[])

    cycles = [
        _load_fixture(f"{fixtures_folder}/{subfolder}/cycle{i}.jsonld") for i in range(num_cycles)
    ]

    _get_site_mock.return_value = site
    related_cycles_mock.return_value = cycles

    result = run(cycle)
    assert order_list(result) == order_list(expected)


@patch(f"{class_path}._new_emission", side_effect=fake_new_emission)
@patch(f"{utils_path}.related_cycles")
@patch(f"{utils_path}._get_site")  # TODO: rationalise order of patches
def test_run_empty(_get_site_mock, related_cycles_mock, _new_emission_mock):
    """
    Test `run` function for each cycle in each scenario.
    """
    CYCLE = {}
    EXPECTED = []

    _get_site_mock.return_value = {}
    related_cycles_mock.return_value = [CYCLE]

    result = run(CYCLE)
    assert result == EXPECTED
