from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import non_empty_list, list_average
from hestia_earth.utils.lookup import extract_grouped_data

from hestia_earth.models.log import logShouldRun, logRequirements, log_as_table
from hestia_earth.models.utils.term import get_lookup_value
from . import MODEL


def run_products_average(cycle: dict, term_id: str, get_value_func):
    products = cycle.get('products', [])

    values_by_product = [
        (p.get('term', {}).get('@id'), get_value_func(p)) for p in products
    ]
    values = non_empty_list([
        value for term_id, value in values_by_product
    ])
    has_values = len(values) > 0

    logRequirements(cycle, model=MODEL, term=term_id,
                    has_values=has_values,
                    details=log_as_table([
                        {'id': term_id, 'value': value} for term_id, value in values_by_product
                    ]))

    should_run = all([has_values])
    logShouldRun(cycle, MODEL, term_id, should_run)
    return list_average(values) if should_run else None


def get_excreta_product(cycle: dict, term: dict, lookup_expected_id: str, lookup_allowed_ids: str):
    primary_excreta_data = get_lookup_value(term, lookup_expected_id, model=MODEL) or (
        # TODO: remove fallback when glossary is fixed for liveAquaticSpecies
        get_lookup_value(term, lookup_expected_id[0:-1], model=MODEL) or ''
    )
    expected_term_id = extract_grouped_data(primary_excreta_data, 'default') if ':' in primary_excreta_data \
        else primary_excreta_data
    allowed_term_ids = (get_lookup_value(term, lookup_allowed_ids, model=MODEL) or '').split(';')
    products = non_empty_list([
        find_term_match(cycle.get('products', []), term_id) for term_id in non_empty_list(
            [expected_term_id] + allowed_term_ids
        )
    ])
    # take the first product available or create a new one with expected id
    return products[0] if products else {
        '@type': 'Product',
        'term': {'@type': 'Term', '@id': expected_term_id}
    }
