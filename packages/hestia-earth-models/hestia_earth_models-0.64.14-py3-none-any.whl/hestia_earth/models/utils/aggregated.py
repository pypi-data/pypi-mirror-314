import math
from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import search
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.model import find_term_match, linked_node
from hestia_earth.utils.tools import safe_parse_date, non_empty_list

from hestia_earth.models.log import debugValues, logShouldRun
from hestia_earth.models.utils.cycle import is_organic

MODEL_KEY = 'impactAssessment'
MATCH_WORLD_QUERY = {'match': {'country.name.keyword': {'query': 'World', 'boost': 1}}}


def aggregated_end_date(end_date: str):
    year = safe_parse_date(end_date).year
    return round(math.floor(year / 10) * 10) + 9


def _match_region_country(region: dict, country: dict):
    region_name = region.get('name') if region else None
    country_name = country.get('name') if country else None
    return {
        'bool': {
            # either get with exact country, or default to global
            'should': non_empty_list([
                (
                    {'match': {'region.name.keyword': {'query': region_name, 'boost': 1000}}} if region_name else
                    {'match': {'country.name.keyword': {'query': country_name, 'boost': 1000}}} if country_name else
                    None
                ),
                MATCH_WORLD_QUERY
            ]),
            'minimum_should_match': 1
        }
    }


def find_closest_impact(cycle: dict, end_date: str, input: dict, region: dict, country: dict, must_queries=[]):
    term = input.get('term', {})
    query = {
        'bool': {
            'must': non_empty_list([
                {'match': {'@type': SchemaType.IMPACTASSESSMENT.value}},
                {'match': {'aggregated': 'true'}},
                {'match': {'aggregatedDataValidated': 'true'}},
                {
                    'bool': {
                        # handle old ImpactAssessment data
                        'should': [
                            {'match': {'product.term.name.keyword': term.get('name')}},
                            {'match': {'product.name.keyword': term.get('name')}}
                        ],
                        'minimum_should_match': 1
                    }
                } if term else None,
                _match_region_country(region, country)
            ]) + must_queries,
            'should': [
                # if the Cycle is organic, we can try to match organic aggregate first
                {'match': {'name': {'query': 'Organic' if is_organic(cycle) else 'Conventional', 'boost': 1000}}},
                {'match': {'endDate': {'query': end_date, 'boost': 1000}}}
            ]
        }
    }
    results = search(query, fields=['@type', '@id', 'name', 'endDate']) if term else []
    # sort by distance to date and score and take min
    results = sorted(
        results,
        key=lambda v: abs(int(end_date) - int(v.get('endDate', '0'))) * v.get('_score', 0),
    )
    return results[0] if len(results) > 0 else None


def _link_input_to_impact(model: str, cycle: dict, date: int):
    def run(input: dict):
        term_id = input.get('term', {}).get('@id')
        region = input.get('region')
        country = input.get('country')
        impact = find_closest_impact(cycle, date, input, region, country)

        debugValues(cycle, model=model, term=term_id, key=MODEL_KEY,
                    input_region=(region or {}).get('@id'),
                    input_country=(country or {}).get('@id'),
                    impact=(impact or {}).get('@id'))

        should_run = all([impact is not None])
        logShouldRun(cycle, model, term_id, should_run)
        logShouldRun(cycle, model, term_id, should_run, key=MODEL_KEY)  # show specifically under Input

        return {**input, MODEL_KEY: linked_node(impact), 'impactAssessmentIsProxy': True} if impact else None
    return run


def link_inputs_to_impact(model: str, cycle: dict, inputs: list):
    date = aggregated_end_date(cycle.get('endDate'))
    return non_empty_list(map(_link_input_to_impact(model, cycle, date), inputs))


def _should_aggregate_input(term: dict):
    lookup = download_lookup(f"{term.get('termType')}.csv", True)
    value = get_table_value(lookup, 'termid', term.get('@id'), column_name('skipAggregation'))
    return True if value is None or value == '' else not value


def should_link_input_to_impact(cycle: dict):
    def should_run(input: dict):
        term = input.get('term', {})
        return all([
            not input.get('impactAssessment'),
            _should_aggregate_input(term),
            # make sure Input is not a Product as well or we might double-count emissions
            find_term_match(cycle.get('products', []), term.get('@id'), None) is None,
            # ignore inputs which are flagged as Product of the Cycle
            not input.get('fromCycle', False),
            not input.get('producedInCycle', False)
        ])
    return should_run
