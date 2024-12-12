from hestia_earth.schema import SiteSiteType
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.tools import safe_parse_float, safe_parse_date

from hestia_earth.models.log import debugMissingLookup, debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, get_site, get_region_id
from hestia_earth.models.utils.cycle import land_occupation_per_kg
from hestia_earth.models.utils.site import get_land_cover_term_id
from . import MODEL


def _get_emission_factor(term_id: str, impact_assessment: dict, average_years: str, from_site_type: SiteSiteType):
    end_date = safe_parse_date(impact_assessment.get('endDate'))

    site = get_site(impact_assessment)
    region_id = get_region_id(impact_assessment)
    to_site_type = site.get('siteType')

    if not to_site_type:
        # site type needed to get factors
        return None

    lookup_name = f"region-{to_site_type.replace(' ', '_')}-landTransformation{average_years}years.csv"
    lookup = download_lookup(lookup_name)
    value = get_table_value(lookup, 'termid', region_id, column_name(from_site_type.value))
    debugMissingLookup(lookup_name, 'termid', region_id, from_site_type.value, value, model=MODEL, term=term_id)

    return safe_parse_float(extract_grouped_data_closest_date(value, end_date.year), None) if end_date else None


def _indicator(term_id: str, value: float, land_covert_term_id: str):
    indicator = _new_indicator(term_id, MODEL, land_covert_term_id)
    indicator['value'] = value
    return indicator


def _run(impact_assessment: dict, term_id: str, land_occupation_m2: float, factor: float):
    land_covert_term_id = get_land_cover_term_id(get_site(impact_assessment).get('siteType'))
    value = land_occupation_m2 * (factor or 0)
    debugValues(impact_assessment, model=MODEL, term=term_id,
                value=value,
                land_covert_term_id=land_covert_term_id)
    return _indicator(term_id, value, land_covert_term_id)


def _should_run(impact_assessment: dict, term_id: str, from_site_type: SiteSiteType, years: int):
    site = get_site(impact_assessment)
    has_site = bool(site)
    cycle = impact_assessment.get('cycle', {})
    product = get_product(impact_assessment)
    site = get_site(impact_assessment)
    land_occupation_m2_kg = land_occupation_per_kg(MODEL, term_id, cycle, site, product)
    land_transformation_factor = _get_emission_factor(term_id, impact_assessment, years, from_site_type)

    logRequirements(impact_assessment, model=MODEL, term=term_id,
                    has_site=has_site,
                    land_occupation_m2_kg=land_occupation_m2_kg,
                    land_transformation_factor=land_transformation_factor)

    should_run = all([
        has_site,
        land_occupation_m2_kg is not None,
        land_occupation_m2_kg == 0 or land_transformation_factor is not None
    ])
    logShouldRun(impact_assessment, MODEL, term_id, should_run)
    return should_run, land_occupation_m2_kg, land_transformation_factor


def run_land_transformation(impact_assessment: dict, term_id: str, from_site_type: SiteSiteType, years: int = 20):
    should_run, land_occupation_m2, factor = _should_run(impact_assessment, term_id, from_site_type, years)
    return [_run(impact_assessment, term_id, land_occupation_m2, factor)] if should_run else []
