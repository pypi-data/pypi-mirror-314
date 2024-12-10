from hestia_earth.utils.tools import non_empty_list

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils import sum_values
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, convert_value_from_cycle
from hestia_earth.models.utils.input import sum_input_impacts
from . import MODEL


def _indicator(term_id: str, value: float):
    indicator = _new_indicator(term_id, MODEL)
    indicator['value'] = value
    return indicator


def _run_inputs_production(impact_assessment: dict, product: dict, term_id: str):
    cycle = impact_assessment.get('cycle', {})
    values_from_cycle = non_empty_list([
        sum_input_impacts(cycle.get('inputs', []), term_id),
        sum_input_impacts(cycle.get('inputs', []), term_id.replace('InputsProduction', 'DuringCycle'))
    ])
    value = convert_value_from_cycle(product, sum_values(values_from_cycle), model=MODEL, term_id=term_id)
    debugValues(impact_assessment, model=MODEL, term=term_id,
                has_values_from_cycle=len(values_from_cycle) > 0)
    logShouldRun(impact_assessment, MODEL, term_id, value is not None)
    return [] if value is None else [_indicator(term_id, value)]


def _should_run_inputs_production(impact_assessment: dict, term_id: str):
    product = get_product(impact_assessment)
    product_id = (product or {}).get('term', {}).get('@id')

    logRequirements(impact_assessment, model=MODEL, term=term_id,
                    product=product_id)

    should_run = all([product])
    return should_run, product


def run_inputs_production(impact_assessment: dict, term_id: str):
    should_run, product = _should_run_inputs_production(impact_assessment, term_id)
    return _run_inputs_production(impact_assessment, product, term_id) if should_run else []
