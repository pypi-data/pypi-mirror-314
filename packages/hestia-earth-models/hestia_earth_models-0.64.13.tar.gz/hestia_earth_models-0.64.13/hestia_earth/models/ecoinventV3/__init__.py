"""
ecoinvent v3

This model calculates background emissions related to the production of Inputs from the ecoinvent database, version 3.

Note: to use the `ecoinventV3` model locally or in the
[HESTIA Community Edition](https://gitlab.com/hestia-earth/hestia-community-edition) you need a valid ecoinvent license.
Please contact us at community@hestia.earth for instructions to download the required file to run the model.

**Pesticide Brand Name**

For `Input` with a [Pesticide Brand Name](https://hestia.earth/glossary?pesticideBrandBane) term, you can override the
default list of [Pesticide Active Ingredient](https://hestia.earth/glossary?pesticideAI) by specifying the list of
[properties](https://hestia.earth/schema/Input#properties) manually.
"""
from functools import reduce
from hestia_earth.schema import EmissionMethodTier
from hestia_earth.utils.tools import flatten, list_sum

from hestia_earth.models.log import debugValues, logShouldRun, logRequirements
from hestia_earth.models.data.ecoinventV3 import ecoinventV3_emissions
from hestia_earth.models.utils import is_from_model
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.blank_node import group_by_keys
from hestia_earth.models.utils.pesticideAI import get_pesticides_from_inputs
from hestia_earth.models.utils.fertiliser import get_fertilisers_from_inputs
from .utils import get_background_inputs, get_input_mappings

REQUIREMENTS = {
    "Cycle": {
        "inputs": [{
            "@type": "Input",
            "value": "> 0",
            "none": {
                "fromCycle": "True",
                "producedInCycle": "True"
            }
        }],
        "optional": {
            "animals": [{
                "@type": "Animal",
                "inputs": [{
                    "@type": "Input",
                    "value": "> 0",
                    "none": {
                        "fromCycle": "True",
                        "producedInCycle": "True"
                    }
                }]
            }]
        }
    }
}
RETURNS = {
    "Emission": [{
        "term": "",
        "value": "",
        "methodTier": "background",
        "inputs": "",
        "operation": "",
        "animals": ""
    }]
}
LOOKUPS = {
    "electricity": "ecoinventMapping",
    "fuel": "ecoinventMapping",
    "inorganicFertiliser": "ecoinventMapping",
    "material": "ecoinventMapping",
    "pesticideAI": "ecoinventMapping",
    "soilAmendment": "ecoinventMapping",
    "transport": "ecoinventMapping",
    "veterinaryDrugs": "ecoinventMapping"
}
MODEL = 'ecoinventV3'
MODEL_KEY = 'impactAssessment'  # keep to generate entry in "model-links.json"
TIER = EmissionMethodTier.BACKGROUND.value


def _emission(term_id: str, value: float, input: dict):
    emission = _new_emission(term_id, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    emission['inputs'] = [input.get('term')]
    if input.get('operation'):
        emission['operation'] = input.get('operation')
    if input.get('animal'):
        emission['animals'] = [input.get('animal')]
    return emission


def _add_emission(cycle: dict, input: dict):
    input_term_id = input.get('term', {}).get('@id')
    operation_term_id = input.get('operation', {}).get('@id')
    animal_term_id = input.get('animal', {}).get('@id')

    def add(prev: dict, mapping: tuple):
        ecoinventName, coefficient = mapping
        emissions = ecoinventV3_emissions(ecoinventName)
        for emission_term_id, value in emissions:
            # log run on each emission so we know it did run
            debugValues(cycle, model=MODEL, term=emission_term_id,
                        value=value,
                        coefficient=coefficient,
                        input=input_term_id,
                        operation=operation_term_id,
                        animal=animal_term_id)
            prev[emission_term_id] = prev.get(emission_term_id, 0) + (value * coefficient)
        return prev
    return add


def _run_input(cycle: dict):
    emissions = cycle.get('emissions', [])

    def run(inputs: list):
        input = inputs[0]
        input_term_id = input.get('term', {}).get('@id')
        operation_term_id = input.get('operation', {}).get('@id')
        animal_term_id = input.get('animal', {}).get('@id')
        input_value = list_sum(flatten(input.get('value', []) for input in inputs))
        mappings = get_input_mappings(MODEL, cycle, input)
        has_mappings = len(mappings) > 0
        # skip input that has background emissions we have already gap-filled (model run before)
        has_no_gap_filled_background_emissions = not any([
            is_from_model(e)
            for e in emissions
            if all([
                any([i.get('@id') == input_term_id for i in e.get('inputs', [])]),
                e.get('operation', {}).get('@id') == operation_term_id,
                e.get('animal', {}).get('@id') == animal_term_id
            ])
        ])

        logRequirements(cycle, model=MODEL, term=input_term_id,
                        has_ecoinvent_mappings=has_mappings,
                        ecoinvent_mappings=';'.join([v[0] for v in mappings]),
                        has_no_gap_filled_background_emissions=has_no_gap_filled_background_emissions)

        should_run = all([has_mappings, has_no_gap_filled_background_emissions])
        logShouldRun(cycle, MODEL, input_term_id, should_run, methodTier=TIER)
        grouped_emissions = reduce(_add_emission(cycle, input), mappings, {}) if should_run else {}
        return [
            _emission(term_id, value * input_value, input)
            for term_id, value in grouped_emissions.items()
        ]
    return run


def run(_, cycle: dict):
    extra_inputs = get_pesticides_from_inputs(cycle) + get_fertilisers_from_inputs(cycle)
    inputs = get_background_inputs(cycle, extra_inputs=extra_inputs)
    grouped_inputs = reduce(group_by_keys(['term', 'operation', 'animal']), inputs, {})
    return flatten(map(_run_input(cycle), grouped_inputs.values()))
