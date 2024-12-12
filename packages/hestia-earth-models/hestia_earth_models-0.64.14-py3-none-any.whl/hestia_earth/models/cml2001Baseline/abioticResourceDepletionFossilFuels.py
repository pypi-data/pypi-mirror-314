"""
This model calculates the abiotic resource depletion, fossil fuels. Based on the models CML 2002 (Guinée et al., 2002) and van Oers et al. 2002 (method, v.4.8)

>The earth contains a finite amount of non-renewable resources, such as fossil fuels like coal, oil and gas. The basic idea behind this impact category is that extracting resources today will force future generations to extract less or different resources. For example, the depletion of V2.0 – 25th August 2023 28 fossil fuels may lead to the non-availability of fossil fuels for future generations. The amount of materials contributing to resource use, fossils, are converted into MJ.

Source : [Life Cycle Assessment & the EF methods - Comprehensive coverage of impacts](https://green-business.ec.europa.eu/environmental-footprint-methods/life-cycle-assessment-ef-methods_en)

The model accepts any non-renewable energy term that can be expressed in, or converted to, MegaJoules.

Source: [JRC Technical reports Suggestions for updating the Product Environmental Footprint (PEF) method](https://eplca.jrc.ec.europa.eu/permalink/PEF_method.pdf#%5B%7B%22num%22%3A80%2C%22gen%22%3A0%7D%2C%7B%22name%22%3A%22XYZ%22%7D%2C68%2C363%2C0%5D)

Source: [Differences between EF model versions](https://eplca.jrc.ec.europa.eu/EFVersioning.html)
"""  # noqa: E501
from itertools import chain
from typing import Optional

from hestia_earth.schema import TermTermType
from hestia_earth.utils.lookup import download_lookup, column_name
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import list_sum, flatten

from hestia_earth.models.log import logShouldRun, logRequirements, log_as_table
from . import MODEL
from ..utils.blank_node import convert_unit
from ..utils.constant import Units
from ..utils.indicator import _new_indicator
from ..utils.lookup import _node_value

REQUIREMENTS = {
    "ImpactAssessment": {
        "emissionsResourceUse": [
            {
                "@type": "Indicator",
                "term.termType": "resourceUse",
                "term.@id": ["resourceUseEnergyDepletionInputsProduction", "resourceUseEnergyDepletionDuringCycle"],
                "value": "> 0",
                "inputs":
                    {
                        "@type": "Input",
                        "term.name": "non-renewable\" energy terms only,\"",
                        "term.units": ["kg", "m3", "kWh", "MJ"],
                        "term.termType": ["fuel", "electricity"],
                        "optional": {
                            "defaultProperties": [
                                {
                                    "@type": "Property",
                                    "value": "",
                                    "term.@id": "energyContentHigherHeatingValue",
                                    "term.units": "MJ / kg"
                                },
                                {
                                    "@type": "Property",
                                    "value": "",
                                    "term.@id": "density",
                                    "term.units": "kg / m3"
                                }
                            ]
                        }
                    }
            }
        ]
    }
}

LOOKUPS = {
    "fuel": ["energyContentHigherHeatingValue", "density", "abioticResourceDepletionFossilFuelsCml2001Baseline"],
    "electricity": ["abioticResourceDepletionFossilFuelsCml2001Baseline"]
}

RETURNS = {
    "Indicator": {
        "value": ""
    }
}
TERM_ID = 'abioticResourceDepletionFossilFuels'

ENERGY_CARRIERS_TERMIDS = REQUIREMENTS['ImpactAssessment']['emissionsResourceUse'][0]['term.@id']

INPUTS_TYPES_UNITS = {
    TermTermType.FUEL.value: [Units.KG.value, Units.M3.value, Units.MJ.value],
    TermTermType.ELECTRICITY.value: [Units.KW_H.value, Units.MJ.value]
}


def download_all_non_renewable_terms(lookup_file_name: str) -> list:
    """
    returns all non renewable term ids in lookup files like `electricity.csv` or `fuel.csv`
    """
    lookup = download_lookup(lookup_file_name)
    results = lookup[
        lookup[column_name("abioticResourceDepletionFossilFuelsCml2001Baseline")] == True  # noqa: E712
        ]["termid"]
    terms_ids: list[str] = [str(entry) for entry in results]
    return terms_ids


def _valid_resource_indicator(resource: dict) -> bool:
    return len(resource.get('inputs', [])) == 1 and \
           isinstance(_node_value(resource), (int, float)) and \
           _node_value(resource) > 0


def _valid_input(input: dict) -> bool:
    return input.get("@id") in list(chain.from_iterable([
        download_all_non_renewable_terms(f"{termType}.csv") for termType in LOOKUPS.keys()
    ])) and input.get("units", "") in INPUTS_TYPES_UNITS.get(input.get("termType", ""))


def _get_value_in_mj(input: dict, indicator: dict) -> Optional[float]:
    return convert_unit(input, dest_unit=Units.MJ, node_value=_node_value(indicator)) if _valid_input(input) else None


def _indicator(value: float):
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator["value"] = value
    return indicator


def _run(energy_resources_in_mj: list):
    return _indicator(list_sum(energy_resources_in_mj))


def _should_run(impact_assessment: dict) -> tuple[bool, list]:
    emissions_resource_use = [
        resource for resource in
        filter_list_term_type(impact_assessment.get('emissionsResourceUse', []), TermTermType.RESOURCEUSE) if
        resource.get('term', {}).get('@id', '') in ENERGY_CARRIERS_TERMIDS]

    has_resource_use_entries = bool(emissions_resource_use)

    resource_uses_unpacked = flatten(
        [
            [
                {
                    "input-term-id": input.get('@id'),
                    "input-term-type": input.get('termType'),
                    "indicator-term-id": resource_indicator['term']['@id'],
                    "indicator-is-valid": _valid_resource_indicator(resource_indicator),
                    "input": input,
                    "indicator-input-is-valid": _valid_input(input),
                    "value": _node_value(resource_indicator),
                    "input-unit": input.get('units'),
                    "value-in-MJ": _get_value_in_mj(input, resource_indicator)
                } for input in resource_indicator['inputs'] or [{}]]
            for resource_indicator in emissions_resource_use
        ]
    )

    has_valid_input_requirements = all([
        all([energy_input['indicator-is-valid'], energy_input['indicator-input-is-valid']])
        for energy_input in resource_uses_unpacked
    ])

    energy_resources_in_mj = [energy_input['value-in-MJ'] for energy_input in resource_uses_unpacked]
    valid_energy_resources_in_mj = [value for value in energy_resources_in_mj if value is not None]
    all_inputs_have_valid_mj_value = all([energy is not None for energy in energy_resources_in_mj]
                                         ) and bool(energy_resources_in_mj)

    logRequirements(impact_assessment, model=MODEL, term=TERM_ID,
                    has_resource_use_entries=has_resource_use_entries,
                    has_valid_input_requirements=has_valid_input_requirements,
                    all_inputs_have_valid_mj_value=all_inputs_have_valid_mj_value,
                    energy_resources_used=log_as_table(resource_uses_unpacked))

    should_run = has_resource_use_entries is False or all([has_resource_use_entries,
                                                           has_valid_input_requirements,
                                                           all_inputs_have_valid_mj_value])

    logShouldRun(impact_assessment, MODEL, TERM_ID, should_run)
    return should_run, valid_energy_resources_in_mj


def run(impact_assessment: dict):
    should_run, resources = _should_run(impact_assessment)
    return _run(resources) if should_run else None
