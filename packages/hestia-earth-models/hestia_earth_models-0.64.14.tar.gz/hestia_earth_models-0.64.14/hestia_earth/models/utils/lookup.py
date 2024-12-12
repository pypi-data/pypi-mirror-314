from typing import Optional, List
from numpy import recarray
from hestia_earth.schema import SchemaType
from hestia_earth.utils.lookup import (
    download_lookup, get_table_value, column_name, extract_grouped_data, _get_single_table_value
)
from hestia_earth.utils.tools import list_sum, safe_parse_float, non_empty_list

from ..log import debugValues, log_as_table, debugMissingLookup


def _node_value(node):
    value = node.get('value')
    return list_sum(value) if isinstance(value, list) else value


def _factor_value(model: str, term_id: str, lookup_name: str, lookup_col: str, grouped_key: Optional[str] = None):
    lookup = download_lookup(lookup_name)

    def get_value(data: dict):
        node_term_id = data.get('term', {}).get('@id')
        grouped_data_key = grouped_key or data.get('methodModel', {}).get('@id')
        value = _node_value(data)
        coefficient = get_table_value(lookup, 'termid', node_term_id, column_name(lookup_col))
        # value is either a number or matching between a model and a value (restrict value to specific model only)
        coefficient = safe_parse_float(
            extract_grouped_data(coefficient, grouped_data_key), None
        ) if ':' in str(coefficient) else safe_parse_float(coefficient, None)
        if value is not None and coefficient is not None:
            if model:
                debugValues(data, model=model, term=term_id,
                            node=node_term_id,
                            operation=data.get('operation', {}).get('@id'),
                            value=value,
                            coefficient=coefficient)
        return {'id': node_term_id, 'value': value, 'coefficient': coefficient}
    return get_value


def all_factor_value(
    model: str,
    term_id: str,
    node: dict,
    lookup_name: str,
    lookup_col: str,
    blank_nodes: List[dict],
    grouped_key: Optional[str] = None,
    default_no_values=0
):
    values = list(map(_factor_value(model, term_id, lookup_name, lookup_col, grouped_key), blank_nodes))

    missing_values = set([v.get('id') for v in values if v.get('value') is not None and v.get('coefficient') is None])
    all_with_factors = all([v.get('coefficient') is not None for v in values if v.get('value') is not None])

    for term_id in missing_values:
        debugMissingLookup(lookup_name, 'termid', term_id, lookup_col, None)

    debugValues(node, model=model, term=term_id,
                all_with_factors=all_with_factors,
                missing_lookup_factor=';'.join(missing_values),
                values_used=log_as_table(values))

    values = [float((v.get('value') or 0) * (v.get('coefficient') or 0)) for v in values]

    # fail if some factors are missing
    return None if not all_with_factors else (
        list_sum(values) if len(values) > 0 else default_no_values
    )


def _term_factor_value(model: str, term_id: str, lookup_name: str, lookup_term_id: str, group_key: str = None):
    lookup = download_lookup(lookup_name, False)  # avoid saving in memory as there could be many different files used

    def get_value(data: dict):
        node_term_id = data.get('term', {}).get('@id')
        value = _node_value(data)
        coefficient = get_table_value(lookup, 'termid', lookup_term_id, column_name(node_term_id))
        coefficient = safe_parse_float(extract_grouped_data(coefficient, group_key) if group_key else coefficient)
        if value is not None and coefficient is not None:
            debugValues(data, model=model, term=term_id, node=node_term_id, value=value, coefficient=coefficient)
        return {'id': node_term_id, 'value': value, 'coefficient': coefficient}
    return get_value


def _aware_factor_value(model: str, term_id: str, lookup_name: str, aware_id: str, group_key: str = None):
    lookup = download_lookup(lookup_name, False)  # avoid saving in memory as there could be many different files used
    lookup_col = column_name('awareWaterBasinId')

    def get_value(data: dict):
        try:
            node_term_id = data.get('term', {}).get('@id')
            value = _node_value(data)
            coefficient = _get_single_table_value(lookup, lookup_col, int(aware_id), column_name(node_term_id))
            coefficient = safe_parse_float(extract_grouped_data(coefficient, group_key)) if group_key else coefficient
            if value is not None and coefficient is not None:
                debugValues(data, model=model, term=term_id, node=node_term_id, value=value, coefficient=coefficient)
                return value * coefficient
            return None
        except ValueError:  # factor does not exist
            return None
    return get_value


_ALLOW_ALL = 'all'


def _is_site(site: dict):
    return site.get('@type', site.get('type')) == SchemaType.SITE.value if site else None


def _get_sites(node: dict):
    site = node.get('site', node.get('cycle', {}).get('site'))
    other_sites = node.get('otherSites', node.get('cycle', {}).get('otherSites', []))
    return non_empty_list([site] + other_sites)


def _get_site_types(node: dict):
    sites = [node] if _is_site(node) else _get_sites(node)
    return non_empty_list([site.get('siteType') for site in sites])


def _model_lookup_values(model: str, term: dict, restriction: str):
    lookup = download_lookup(f"{term.get('termType')}-model-{restriction}.csv")
    values = get_table_value(lookup, 'termid', term.get('@id'), column_name(model))
    return (values or _ALLOW_ALL).split(';') if isinstance(values, str) else _ALLOW_ALL


def is_model_siteType_allowed(model: str, term: dict, data: dict):
    site_types = _get_site_types(data)
    allowed_values = _model_lookup_values(model, term, 'siteTypesAllowed')
    return True if _ALLOW_ALL in allowed_values or not site_types else any([
        (site_type in allowed_values) for site_type in site_types
    ])


def _lookup_values(term: dict, column: str):
    lookup = download_lookup(f"{term.get('termType')}.csv")
    values = get_table_value(lookup, 'termid', term.get('@id'), column_name(column))
    return (values or _ALLOW_ALL).split(';') if isinstance(values, str) else _ALLOW_ALL


def is_siteType_allowed(data: dict, term: dict):
    site_types = _get_site_types(data)
    allowed_values = _lookup_values(term, 'siteTypesAllowed')
    return True if _ALLOW_ALL in allowed_values or not site_types else any([
        (site_type in allowed_values) for site_type in site_types
    ])


def is_product_termType_allowed(data: dict, term: dict):
    products = data.get('products', [])
    values = non_empty_list([p.get('term', {}).get('termType') for p in products])
    allowed_values = _lookup_values(term, 'productTermTypesAllowed')
    return True if any([
        _ALLOW_ALL in allowed_values,
        len(values) == 0
    ]) else any([value in allowed_values for value in values])


def is_product_id_allowed(data: dict, term: dict):
    products = data.get('products', [])
    values = non_empty_list([p.get('term', {}).get('@id') for p in products])
    allowed_values = _lookup_values(term, 'productTermIdsAllowed')
    return True if any([
        _ALLOW_ALL in allowed_values,
        len(values) == 0
    ]) else any([value in allowed_values for value in values])


def is_input_termType_allowed(data: dict, term: dict):
    inputs = data.get('inputs', [])
    values = non_empty_list([p.get('term', {}).get('termType') for p in inputs])
    allowed_values = _lookup_values(term, 'inputTermTypesAllowed')
    return True if any([
        _ALLOW_ALL in allowed_values,
        len(values) == 0
    ]) else any([value in allowed_values for value in values])


def is_input_id_allowed(data: dict, term: dict):
    inputs = data.get('inputs', [])
    values = non_empty_list([p.get('term', {}).get('@id') for p in inputs])
    allowed_values = _lookup_values(term, 'inputTermIdsAllowed')
    return True if any([
        _ALLOW_ALL in allowed_values,
        len(values) == 0
    ]) else any([value in allowed_values for value in values])


def fallback_country(country_id: str, lookup_arrays: List[recarray]) -> str:
    """
    Given a site dict with 'country_id' location term, and lookup table,
    checks if a location can be used in lookup file
    else fallback to the default "region-world"
    """
    is_in_lookup = lambda v: all(v in array['termid'] for array in lookup_arrays)  # noqa: E731
    fallback_id = 'region-world'
    return country_id if is_in_lookup(country_id) else fallback_id if is_in_lookup(fallback_id) else None
