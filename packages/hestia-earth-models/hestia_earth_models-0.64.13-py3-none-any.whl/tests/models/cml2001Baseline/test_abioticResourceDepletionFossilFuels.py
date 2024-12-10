import json
from unittest.mock import patch

from pytest import mark

from hestia_earth.models.cml2001Baseline.abioticResourceDepletionFossilFuels import MODEL, TERM_ID, run, _should_run, \
    download_all_non_renewable_terms
from tests.utils import fixtures_path, fake_new_indicator

class_path = f"hestia_earth.models.{MODEL}.{TERM_ID}"
fixtures_folder = f"{fixtures_path}/{MODEL}/{TERM_ID}"


def fake_rounded_indicator(value: float):
    indicator = fake_new_indicator(TERM_ID, MODEL)
    indicator['value'] = round(value, 7)
    return indicator


def fake_download_hestia(filename):
    data = {
        'fuel.csv': ["lignite", "conventionalCrudeOil", "naturalGas", "coalTar"],
        'electricity.csv': ['electricityGridMarketMix', 'electricityGridHardCoal', 'electricityProducedOnSiteHardCoal',
                            'electricityGridNaturalGas', 'electricityProducedOnSiteNaturalGas', 'electricityGridOil',
                            'electricityProducedOnSiteOil', 'electricityGridNuclear']}
    return data[filename]


input_lignite_mj = {"@id": "lignite", "name": "lignite (Brown coal)", "termType": "fuel", "units": "MJ"}
input_coal_tar_kg = {"@id": "coalTar", "name": "Coal tar unknown energy Content", "termType": "fuel", "units": "kg"}
input_crude_oil_kg_property = {
    "@id": "conventionalCrudeOil", "name": "Conventional Crude Oil", "termType": "fuel", "units": "kg",
    "properties": [{"@type": "Property", "value": 45.8,
                    "term": {"@type": "Term", "@id": "energyContentHigherHeatingValue", "units": "MJ / kg"}, }]}
input_crude_oil_kg_no_property = {
    "@id": "conventionalCrudeOil", "name": "Conventional Crude Oil", "termType": "fuel", "units": "kg"}
input_natural_gas_m3 = {"@id": "naturalGas", "name": "Natural Gas", "termType": "fuel", "units": "m3"}
input_nuclear_fuel_mj = {"@id": "electricityGridNuclear", "name": "Any depleted nuclear fuel",
                         "termType": "electricity", "units": "MJ"}
input_nuclear_fuel_kwh = {"@id": "electricityGridNuclear", "termType": "electricity", "units": "kWh"}
input_excessIndustrialHeat_mj = {"@id": "excessIndustrialHeat", "name": "Excess industrial heat", "termType": "fuel",
                                 "units": "MJ"}

wrong_indicator = {"term": {"@id": "BAD_INDICATOR_ID", "termType": "resourceUse"},
                   "value": 5,
                   "inputs": [input_lignite_mj]}

indicator_no_inputs = {"term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
                       "value": 5,
                       "inputs": []}

indicator_2_inputs = {"term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
                      "value": 5,
                      "inputs": [input_lignite_mj, input_lignite_mj]}

indicator_no_unit = {"term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
                     "value": 5,
                     "inputs": [{
                         "@id": "lignite",
                         "@type": "Term",
                         "name": "lignite (Brown coal)",
                         "termType": "fuel",
                     }]}

indicator_wrong_unit = {"term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
                        "value": 5,
                        "inputs": [
                            {
                                "@id": "lignite",
                                "@type": "Term",
                                "name": "lignite (Brown coal)",
                                "termType": "fuel",
                                "units": "ha"
                            }
                        ]}

indicator_bad_input_id = {"term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
                          "value": 5,
                          "inputs": [input_excessIndustrialHeat_mj]}

good_indicator_inputs_production_mj = {
    "term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
    "value": 5,
    "inputs": [input_lignite_mj]
}

good_indicator_during_cycle_mj = {"term": {"@id": "resourceUseEnergyDepletionDuringCycle", "termType": "resourceUse"},
                                  "value": 5,
                                  "inputs": [input_lignite_mj]}

good_indicator_inputs_production_with_property = {
    "term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
    "value": 5,
    "inputs": [input_crude_oil_kg_property]
}

good_indicator_inputs_production_with_no_property = {
    "term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
    "value": 5,
    "inputs": [input_crude_oil_kg_no_property]
}

good_indicator_m3 = {"term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
                     "value": 5,
                     "inputs": [input_natural_gas_m3]}

good_nuclear_indicator_mj = {"term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
                             "value": 5,
                             "inputs": [input_nuclear_fuel_mj]}
good_nuclear_indicator_kwh = {"term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
                              "value": 1.3889,
                              "inputs": [input_nuclear_fuel_kwh]}

bad_fuel_indicator_no_property_lookup = {
    "term": {"@id": "resourceUseEnergyDepletionInputsProduction", "termType": "resourceUse"},
    "value": 5,
    "inputs": [input_coal_tar_kg]}


@mark.parametrize(
    "resources, expected, num_inputs",
    [
        ([], True, 0),
        ([wrong_indicator], True, 0),
        ([indicator_no_inputs], False, 0),
        ([indicator_2_inputs], False, 2),
        ([indicator_no_unit], False, 0),
        ([indicator_wrong_unit], False, 0),
        ([indicator_bad_input_id], False, 0),
        ([good_indicator_inputs_production_mj], True, 1),
        ([good_indicator_during_cycle_mj], True, 1),
        ([good_indicator_inputs_production_with_property], True, 1),
        ([good_indicator_inputs_production_with_no_property], True, 1),
        ([good_indicator_m3], True, 1),
        ([good_nuclear_indicator_mj], True, 1),
        ([good_nuclear_indicator_kwh], True, 1),
        ([bad_fuel_indicator_no_property_lookup], False, 0),
    ],
    ids=["No indicators", "wrong indicator", "indicator no inputs", "indicator 2 inputs", "missing unit", "wrong unit",
         "input id not in requirements", "good input production mj", "good during cycle mj",
         "good input with input property", "good input with no input property", "good indicator in m^3",
         "good nuclear fuel use indicator in mj", "good nuclear fuel use indicator in kWh",
         "bad indicator input in kg no property to convert to mj"]
)
@patch(f"{class_path}.download_all_non_renewable_terms", side_effect=fake_download_hestia)
def test_should_run(mock_download_all_non_renewable_terms, resources, expected, num_inputs):
    with open(f"{fixtures_folder}/impactassessment.jsonld", encoding='utf-8') as f:
        impactassessment = json.load(f)

    impactassessment['emissionsResourceUse'] = resources

    should_run, resources = _should_run(impactassessment)
    assert should_run is expected
    assert len(resources) == num_inputs


@patch(f"{class_path}.download_all_non_renewable_terms", side_effect=fake_download_hestia)
@patch(f"{class_path}._indicator", side_effect=fake_rounded_indicator)
def test_run(*args):
    with open(f"{fixtures_folder}/impactassessment.jsonld", encoding='utf-8') as f:
        impactassessment = json.load(f)

    with open(f"{fixtures_folder}/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(impactassessment)
    assert value == expected


@patch(f"{class_path}._new_indicator", side_effect=fake_new_indicator)
def test_run_no_emissions(*args):
    """
    Impact assessment with no emissions should return a indicator of 0
    """
    with open(f"{fixtures_folder}/impactassessment.jsonld", encoding='utf-8') as f:
        impactassessment = json.load(f)

    del impactassessment['emissionsResourceUse']

    value = run(impactassessment)
    assert value['value'] == 0


def test_download_all_non_renewable_terms(*args):
    """
    make sure download_all_non_renewable_terms() only returns terms we want
    """
    electricity_terms = download_all_non_renewable_terms("electricity.csv")

    assert "electricityGridHardCoal" in electricity_terms
    assert "electricityGridWind" not in electricity_terms

    fuel_terms = download_all_non_renewable_terms("fuel.csv")

    assert "coalTar" in fuel_terms
    assert "sodPeat" not in fuel_terms
