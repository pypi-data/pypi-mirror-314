"""
Input HESTIA Aggregated Data

This model adds `impactAssessment` to inputs based on data which has been aggregated into country level averages.
Note: to get more accurate impacts, we recommend setting the
[input.impactAssessment](https://hestia.earth/schema/Input#impactAssessment)
instead of the region-level averages using this model.
"""
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_primary_product, find_term_match, linked_node

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.crop import valid_site_type
from hestia_earth.models.utils.term import get_generic_crop
from hestia_earth.models.utils.aggregated import (
    should_link_input_to_impact, link_inputs_to_impact, find_closest_impact, aggregated_end_date
)

REQUIREMENTS = {
    "Cycle": {
        "inputs": [{
            "@type": "Input",
            "value": "",
            "none": {
                "impactAssessment": "",
                "fromCycle": "True",
                "producedInCycle": "True"
            },
            "optional": {
                "country": {"@type": "Term", "termType": "region"},
                "region": {"@type": "Term", "termType": "region"}
            }
        }],
        "optional": {
            "site": {
                "@type": "Site",
                "siteType": ["cropland", "pasture"],
                "country": {"@type": "Term", "termType": "region"}
            },
            "inputs": [{
                "@type": "Input",
                "term.@id": "seed",
                "value": "",
                "none": {
                    "impactAssessment": ""
                }
            }],
            "products": [{"@type": "Product", "value": "", "primary": "True"}]
        }
    }
}
RETURNS = {
    "Input": [{
        "impactAssessment": "",
        "impactAssessmentIsProxy": "True"
    }]
}
MODEL_ID = 'hestiaAggregatedData'
MODEL_KEY = 'impactAssessment'
SEED_TERM_ID = 'seed'


def _run_seed(cycle: dict, primary_product: dict, seed_input: dict):
    region = seed_input.get('region')
    country = seed_input.get('country')
    # to avoid double counting seed => aggregated impact => seed, we need to get the impact of the previous decade
    # if the data does not exist, use the aggregated impact of generic crop instead
    date = aggregated_end_date(cycle.get('endDate'))
    impact = find_closest_impact(cycle, date, primary_product, region, country, [
        {'match': {'endDate': date - 10}}
    ]) or find_closest_impact(cycle, date, {'term': get_generic_crop()}, region, country)

    debugValues(cycle, model=MODEL_ID, term=SEED_TERM_ID, key=MODEL_KEY,
                input_region=(region or {}).get('@id'),
                input_country=(country or {}).get('@id'),
                date=date,
                impact=(impact or {}).get('@id'))

    return [{**seed_input, MODEL_KEY: linked_node(impact), 'impactAssessmentIsProxy': True}] if impact else []


def _should_run_seed(cycle: dict):
    primary_product = find_primary_product(cycle) or {}
    product_id = primary_product.get('term', {}).get('@id')
    term_type = primary_product.get('term', {}).get('termType')
    is_crop_product = term_type == TermTermType.CROP.value
    input = find_term_match(cycle.get('inputs', []), SEED_TERM_ID, None)
    has_input = input is not None
    site_type_valid = valid_site_type(cycle, True)

    should_run = all([site_type_valid, is_crop_product, has_input])

    # ignore logs if seed is not present
    if has_input:
        debugValues(cycle, model=MODEL_ID, term=SEED_TERM_ID, key=MODEL_KEY,
                    primary_product_id=product_id,
                    primary_product_term_type=term_type)

        logRequirements(cycle, model=MODEL_ID, term=SEED_TERM_ID, key=MODEL_KEY,
                        site_type_valid=site_type_valid,
                        is_crop_product=is_crop_product,
                        has_input=has_input)

        logShouldRun(cycle, MODEL_ID, SEED_TERM_ID, should_run)
        logShouldRun(cycle, MODEL_ID, SEED_TERM_ID, should_run, key=MODEL_KEY)  # show specifically under Input

    return should_run, primary_product, input


def _should_run(cycle: dict):
    end_date = cycle.get('endDate')
    inputs = cycle.get('inputs', [])
    inputs = list(filter(should_link_input_to_impact(cycle), inputs))
    nb_inputs = len(inputs)

    logRequirements(cycle, model=MODEL_ID, key=MODEL_KEY,
                    end_date=end_date,
                    nb_inputs=nb_inputs)

    should_run = all([end_date, nb_inputs > 0])
    logShouldRun(cycle, MODEL_ID, None, should_run, key=MODEL_KEY)
    return should_run, inputs


def run(cycle: dict):
    should_run, inputs = _should_run(cycle)
    should_run_seed, primary_product, seed_input = _should_run_seed(cycle)
    return (
        link_inputs_to_impact(MODEL_ID, cycle, inputs) if should_run else []
    ) + (
        _run_seed(cycle, primary_product, seed_input) if should_run_seed else []
    )
