from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_sum, flatten, non_empty_list

from hestia_earth.models.utils.term import get_lookup_value


def _animal_inputs(animal: dict):
    inputs = animal.get('inputs', [])
    return [(input | {'animal': animal.get('term', {})}) for input in inputs]


def _should_run_input(products: list):
    def should_run(input: dict):
        return all([
            list_sum(input.get('value', [])) > 0,
            # make sure Input is not a Product as well or we might double-count emissions
            find_term_match(products, input.get('term', {}).get('@id'), None) is None,
            # ignore inputs which are flagged as Product of the Cycle
            not input.get('fromCycle', False),
            not input.get('producedInCycle', False)
        ])
    return should_run


def get_background_inputs(cycle: dict, extra_inputs: list = []):
    # add all the properties of some Term that inlcude others with the mapping
    inputs = flatten(
        cycle.get('inputs', []) +
        list(map(_animal_inputs, cycle.get('animals', []))) +
        extra_inputs
    )
    return list(filter(_should_run_input(cycle.get('products', [])), inputs))


def get_input_mappings(model: str, cycle: dict, input: dict):
    term = input.get('term', {})
    term_id = term.get('@id')
    value = get_lookup_value(term, 'ecoinventMapping', model=model, term=term_id)
    mappings = non_empty_list(value.split(';')) if value else []
    return [(m.split(':')[0], float(m.split(':')[1])) for m in mappings]
