"""
Management node

This model provides data gap-filled data from cycles in the form of a list of management nodes
(https://www.hestia.earth/schema/Management).

It includes products of type crop, forage, landCover (gap-filled with a value of 100) and practices of type waterRegime,
tillage, cropResidueManagement and landUseManagement.

All values are copied from the source node, except for crop and forage terms in which case the dates are copied from the
cycle.

When nodes are chronologically consecutive with "% area" or "boolean" units and the same term and value, they are
condensed into a single node to aid readability.
"""
from functools import reduce
from hestia_earth.schema import TermTermType, SiteSiteType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import safe_parse_float, flatten
from hestia_earth.utils.blank_node import get_node_value

from hestia_earth.models.log import logRequirements, logShouldRun, log_as_table
from hestia_earth.models.utils import _include
from hestia_earth.models.utils.management import _new_management
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.blank_node import condense_nodes
from hestia_earth.models.utils.site import (
    related_cycles, get_land_cover_term_id as get_landCover_term_id_from_site_type
)
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "related": {
            "Cycle": [{
                "@type": "Cycle",
                "startDate": "",
                "endDate": "",
                "products": [
                    {
                        "@type": "Product",
                        "term.termType": ["crop", "forage", "landCover"],
                        "units": ["% area", "boolean"]
                    }
                ],
                "practices": [
                    {
                        "term.termType": [
                            "waterRegime",
                            "tillage",
                            "cropResidueManagement",
                            "landUseManagement",
                            "system"
                        ],
                        "units": ["% area", "boolean"],
                        "value": ""
                    }
                ],
                "inputs": [
                    {
                        "@type": "Input",
                        "term.termType": [
                            "inorganicFertiliser",
                            "organicFertiliser",
                            "soilAmendment"
                        ]
                    }
                ]
            }]
        }
    }
}
RETURNS = {
    "Management": [{
        "@type": "Management",
        "term.termType": [
            "landCover", "waterRegime", "tillage", "cropResidueManagement", "landUseManagement", "system"
        ],
        "value": "",
        "endDate": "",
        "startDate": ""
    }]
}
LOOKUPS = {
    "crop": ["landCoverTermId"],
    "forage": ["landCoverTermId"],
    "inorganicFertiliser": "nitrogenContent",
    "organicFertiliser": "ANIMAL_MANURE",
    "soilAmendment": "PRACTICE_INCREASING_C_INPUT",
    "landUseManagement": "GAP_FILL_TO_MANAGEMENT"
}
MODEL_KEY = 'management'

_LAND_COVER_KEY = LOOKUPS['crop'][0]
_ANIMAL_MANURE_USED_TERM_ID = "animalManureUsed"
_INORGANIC_NITROGEN_FERTILISER_USED_TERM_ID = "inorganicNitrogenFertiliserUsed"
_ORGANIC_FERTILISER_USED_TERM_ID = "organicFertiliserUsed"
_AMENDMENT_INCREASING_C_USED_TERM_ID = "amendmentIncreasingSoilCarbonUsed"
_INPUT_RULES = {
    TermTermType.INORGANICFERTILISER.value: (
        (
            TermTermType.INORGANICFERTILISER.value,  # Lookup column
            lambda x: safe_parse_float(x) > 0,  # Condition
            _INORGANIC_NITROGEN_FERTILISER_USED_TERM_ID  # New term.
        ),
    ),
    TermTermType.SOILAMENDMENT.value: (
        (
            TermTermType.SOILAMENDMENT.value,
            lambda x: bool(x) is True,
            _AMENDMENT_INCREASING_C_USED_TERM_ID
        ),
    ),
    TermTermType.ORGANICFERTILISER.value: (
        (
            TermTermType.SOILAMENDMENT.value,
            lambda x: bool(x) is True,
            _ORGANIC_FERTILISER_USED_TERM_ID
        ),
        (
            TermTermType.ORGANICFERTILISER.value,
            lambda x: bool(x) is True,
            _ANIMAL_MANURE_USED_TERM_ID
        )
    )
}
_SKIP_LAND_COVER_SITE_TYPES = [
    SiteSiteType.CROPLAND.value
]


def management(data: dict):
    node = _new_management(data.get('id'))
    node['value'] = data['value']
    node['endDate'] = data['endDate']
    if data.get('startDate'):
        node['startDate'] = data['startDate']
    if data.get('properties'):
        node['properties'] = data['properties']
    return node


def _map_to_value(value: dict):
    return {
        'id': value.get('term', {}).get('@id'),
        'value': value.get('value'),
        'startDate': value.get('startDate'),
        'endDate': value.get('endDate'),
        'properties': value.get('properties')
    }


def _extract_node_value(node: dict) -> dict:
    return node | {'value': get_node_value(node)}


def _default_dates(cycle: dict, values: list):
    return [(_include(cycle, ["startDate", "endDate"]) | v) for v in values]


def _dates_from_current_cycle(cycle: dict, values: list) -> list:
    """Always uses the dates from the cycle."""
    return [v | _include(cycle, ["startDate", "endDate"]) for v in values]


def _copy_item_if_exists(source: dict, keys: list[str] = None, dest: dict = None) -> dict:
    keys = keys or []
    dest = dest or {}
    return reduce(lambda p, c: p | ({c: source[c]} if c in source else {}), keys, dest)


def _get_landCover_term_id(product: dict) -> str:
    term = product.get('term', {})
    value = get_lookup_value(term, _LAND_COVER_KEY, model=MODEL, term=term.get('@id'), model_key=MODEL_KEY)
    return value.split(';')[0] if value else None


def _get_relevant_items(
    cycle: dict, item_name: str, relevant_terms: list, date_fill: callable = _default_dates
):
    """
    Get items from the list of cycles with any of the relevant terms.
    Also adds dates if missing.
    """
    return [
        item
        for item in date_fill(cycle=cycle, values=filter_list_term_type(cycle.get(item_name, []), relevant_terms))
    ]


def _process_rule(node: dict, term: dict) -> list:
    relevant_terms = []
    for column, condition, new_term in _INPUT_RULES[term.get('termType')]:
        lookup_result = get_lookup_value(term, LOOKUPS[column], model=MODEL, term=term.get('@id'), model_key=MODEL_KEY)

        if condition(lookup_result):
            relevant_terms.append(node | {'id': new_term})

    return relevant_terms


def _run_from_inputs(site: dict, cycle: dict) -> list:
    inputs = flatten([
        _process_rule(node={
            'value': True,
            'startDate': cycle.get('startDate'),
            'endDate': cycle.get('endDate')
        }, term=input.get('term'))
        for input in cycle.get('inputs', [])
        if input.get('term', {}).get('termType') in _INPUT_RULES
    ])
    return inputs


def _run_from_siteType(site: dict, cycle: dict):
    site_type = site.get('siteType')
    site_type_id = get_landCover_term_id_from_site_type(site_type) if site_type not in _SKIP_LAND_COVER_SITE_TYPES \
        else None

    should_run = all([site_type_id])
    return [{
        'id': site_type_id,
        'value': 100,
        'startDate': cycle.get('startDate'),
        'endDate': cycle.get('endDate')
    }] if should_run else []


def _run_from_landCover(cycle: dict):
    products = _get_relevant_items(
        cycle=cycle,
        item_name="products",
        relevant_terms=[TermTermType.LANDCOVER]
    )
    products = [
        _map_to_value(_extract_node_value(
            _include(
                value=product,
                keys=["term", "value", "startDate", "endDate", "properties"]
            )
        )) for product in products
    ]
    return products


def _run_from_crop_forage(cycle: dict):
    products = _get_relevant_items(
        cycle=cycle,
        item_name="products",
        relevant_terms=[TermTermType.CROP, TermTermType.FORAGE],
        date_fill=_dates_from_current_cycle
    )
    products = list(filter(_get_landCover_term_id, products))
    products = [
        _map_to_value(_copy_item_if_exists(
            source=product,
            keys=["startDate", "endDate", "properties"],
            dest={
                "term": {'@id': _get_landCover_term_id(product)},
                "value": round(100 / len(products), 2)
            }
        ))
        for product in products
    ]
    return products


def _has_gap_fill_to_management_set(practice: dict):
    """
    Include only landUseManagement practices where GAP_FILL_TO_MANAGEMENT = True
    """
    term = practice.get('term', {})
    return (
        term.get('termType') != TermTermType.LANDUSEMANAGEMENT.value or
        get_lookup_value(lookup_term=term, column=LOOKUPS["landUseManagement"])
    )


def _run_from_practices(cycle: dict):
    practices = [
        _extract_node_value(
            _include(
                value=practice,
                keys=["term", "value", "startDate", "endDate"]
            )
        ) for practice in _get_relevant_items(
            cycle=cycle,
            item_name="practices",
            relevant_terms=[
                TermTermType.WATERREGIME,
                TermTermType.TILLAGE,
                TermTermType.CROPRESIDUEMANAGEMENT,
                TermTermType.LANDUSEMANAGEMENT,
                TermTermType.SYSTEM
            ]
        )
    ]
    practices = list(map(_map_to_value, filter(_has_gap_fill_to_management_set, practices)))
    return practices


def _run_cycle(site: dict, cycle: dict):
    inputs = _run_from_inputs(site, cycle)
    products = _run_from_landCover(cycle) + _run_from_crop_forage(cycle)
    site_types = _run_from_siteType(site, cycle)
    practices = _run_from_practices(cycle)
    return [
        node | {'cycle-id': cycle.get('@id')}
        for node in inputs + products + site_types + practices
    ]


def run(site: dict):
    cycles = related_cycles(site)
    nodes = flatten([_run_cycle(site, cycle) for cycle in cycles])

    # group nodes with same `id` to display as a single log per node
    grouped_nodes = reduce(lambda p, c: p | {c['id']: p.get(c['id'], []) + [c]}, nodes, {})
    for id, values in grouped_nodes.items():
        logRequirements(
            site,
            model=MODEL,
            term=id,
            model_key=MODEL_KEY,
            details=log_as_table(values, ignore_keys=['id', 'properties']),
        )
        logShouldRun(site, MODEL, id, True, model_key=MODEL_KEY)

    management_nodes = condense_nodes(list(map(management, nodes)))
    return management_nodes
