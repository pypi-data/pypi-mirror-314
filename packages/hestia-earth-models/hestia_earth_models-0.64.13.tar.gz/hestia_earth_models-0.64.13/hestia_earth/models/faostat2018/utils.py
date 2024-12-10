from hestia_earth.schema import TermTermType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.tools import safe_parse_float
from numpy import recarray

from hestia_earth.models.log import logger, debugMissingLookup
from hestia_earth.models.utils.animalProduct import (
    FAO_LOOKUP_COLUMN, FAO_EQUIVALENT_LOOKUP_COLUMN, get_animalProduct_lookup_value
)
from hestia_earth.models.utils.product import convert_product_to_unit
from . import MODEL

LOOKUP_PREFIX = f"{TermTermType.REGION.value}-{TermTermType.ANIMALPRODUCT.value}-{FAO_LOOKUP_COLUMN}"


def get_liveAnimal_to_animalProduct_id(product_term_id: str, column: str, **log_args):
    lookup_name = 'liveAnimal.csv'
    lookup = download_lookup(lookup_name)
    value = get_table_value(lookup, 'termid', product_term_id, column_name(column))
    debugMissingLookup(lookup_name, 'termid', product_term_id, column, value, model=MODEL, **log_args)
    return value


def product_equivalent_value(product: dict, year: int, country: str):
    term_id = product.get('term', {}).get('@id')
    fao_product_id = get_animalProduct_lookup_value(MODEL, term_id, FAO_EQUIVALENT_LOOKUP_COLUMN) or term_id
    grouping = get_animalProduct_lookup_value(MODEL, fao_product_id, FAO_LOOKUP_COLUMN)

    if not grouping or not fao_product_id:
        return None

    lookup = download_lookup(f"{LOOKUP_PREFIX}-productionQuantity.csv")
    quantity_values = get_table_value(lookup, 'termid', country, column_name(grouping))
    quantity = safe_parse_float(extract_grouped_data_closest_date(quantity_values, year))

    lookup = download_lookup(f"{LOOKUP_PREFIX}-head.csv")
    head_values = get_table_value(lookup, 'termid', country, column_name(grouping))
    head = safe_parse_float(extract_grouped_data_closest_date(head_values, year))

    # quantity is in Tonnes
    value = quantity * 1000 / head if head > 0 else 0

    fao_product_term = download_hestia(fao_product_id)
    fao_product = {'term': fao_product_term, 'value': [value]}

    # use the FAO value to convert it to the correct unit
    dest_unit = product.get('term', {}).get('units')
    conv_value = convert_product_to_unit(fao_product, dest_unit)

    logger.debug('model=%s, country=%s, grouping=%s, year=%s, quantity=%s, head=%s, value=%s, conv_value=%s',
                 MODEL, country, f"'{grouping}'", year, quantity, head, value, conv_value)

    return conv_value


def _split_delta(table_value: str, start_year: int, end_year: int):
    start_value = extract_grouped_data_closest_date(table_value, start_year)
    end_value = extract_grouped_data_closest_date(table_value, end_year)
    return safe_parse_float(end_value) - safe_parse_float(start_value) if all([
        start_value is not None, end_value is not None
    ]) else None


def get_sum_of_columns(lookup: recarray, country: str, year: int, columns_list: list) -> float:
    return sum(
        [safe_parse_float(
            extract_grouped_data_closest_date(
                data=get_table_value(lookup, 'termid', country, column_name(col)),
                year=year
            )
        ) for col in columns_list]
    )


def get_single_delta(country: str, start_year: int, end_year: int, column: str):
    lookup = download_lookup('region-faostatArea.csv')
    return _split_delta(
        get_table_value(lookup, 'termid', country, column_name(column)), start_year, end_year
    )


def get_land_ratio(
    country: str, start_year: int, end_year: int, first_column: str, second_column: str, total_column: str = None
):
    """
    total_column is optional. Assumes that, if missing, total is the sum of values from first and second.
    """
    lookup = download_lookup('region-faostatArea.csv')
    first_delta = _split_delta(
        get_table_value(lookup, 'termid', country, column_name(first_column)), start_year, end_year
    )
    second_delta = _split_delta(
        get_table_value(lookup, 'termid', country, column_name(second_column)), start_year, end_year
    )
    total_delta = (
        get_sum_of_columns(
            lookup=lookup,
            country=country,
            year=end_year,
            columns_list=[first_column, second_column]
        ) - get_sum_of_columns(
            lookup=lookup,
            country=country,
            year=start_year,
            columns_list=[first_column, second_column]
        )
    ) if total_column is None else _split_delta(
        get_table_value(lookup, 'termid', country, column_name(total_column)), start_year, end_year
    )

    return (None, None, None) if any([
        total_delta is None,
        first_delta is None,
        second_delta is None
    ]) else (total_delta, first_delta, second_delta)


def get_cropland_ratio(country: str, start_year: int, end_year: int):
    return get_land_ratio(
        country=country,
        start_year=start_year,
        end_year=end_year,
        first_column='Permanent crops',
        second_column='Arable land',
        total_column='Cropland'
    )


def get_change_in_harvested_area_for_crop(country_id: str, crop_name: str, start_year: int, end_year: int = 0):
    lookup = download_lookup('region-crop-cropGroupingFaostatProduction-areaHarvested.csv')
    if end_year == 0 or end_year == start_year:
        return safe_parse_float(
            extract_grouped_data_closest_date(
                data=get_table_value(lookup, 'termid', country_id, column_name(crop_name)),
                year=start_year
            )
        )
    else:
        return _split_delta(
            get_table_value(lookup, 'termid', country_id, column_name(crop_name)), start_year, end_year
        )
