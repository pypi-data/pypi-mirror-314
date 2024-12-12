from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data
from hestia_earth.utils.tools import safe_parse_float

from hestia_earth.models.log import debugMissingLookup
from hestia_earth.models.utils.cycle import cycle_end_year

EMBER_ECOINVENT_LOOKUP_NAME = "ember-ecoinvent-mapping.csv"
REGION_EMBER_SOURCES_LOOKUP_NAME = "region-ember-energySources.csv"


def get_input_coefficient(model: str, cycle: dict, country_id: str, ecoinventName: str):
    year = cycle_end_year(cycle)

    # find the matching ember source with the ecoinventName.
    # example: "electricity, high voltage, electricity production, hard coal" > "Coal"
    ember_ecoinvent_lookup = download_lookup(EMBER_ECOINVENT_LOOKUP_NAME)
    source_name = get_table_value(ember_ecoinvent_lookup, column_name('ecoinventName'), ecoinventName, 'ember')

    # find the ratio for the country / year
    region_ember_sources_lookup = download_lookup(REGION_EMBER_SOURCES_LOOKUP_NAME)
    data = get_table_value(region_ember_sources_lookup, 'termid', country_id, column_name(source_name))
    percentage = extract_grouped_data(data, str(year))
    debugMissingLookup(REGION_EMBER_SOURCES_LOOKUP_NAME,
                       'termid', country_id, source_name, percentage, year=year, model=model)

    return safe_parse_float(percentage, 0) / 100
