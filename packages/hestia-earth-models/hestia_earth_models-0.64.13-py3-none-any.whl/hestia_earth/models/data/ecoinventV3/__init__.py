import os
from hestia_earth.utils.lookup import column_name, get_table_value, load_lookup
from hestia_earth.utils.tools import non_empty_list

from hestia_earth.models.log import logger

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ECOINVENT_FILEPATH = os.getenv('ECOINVENT_V3_FILEPATH', f"{os.path.join(CURRENT_DIR, 'ecoinventV3_excerpt')}.csv")


def _get_file():
    if not os.path.exists(ECOINVENT_FILEPATH):
        logger.warn('Ecoinvent file not found. Please make sure to set env variable "ECOINVENT_V3_FILEPATH".')
        return None

    return load_lookup(filepath=ECOINVENT_FILEPATH, keep_in_memory=True)


def ecoinventV3_emissions(ecoinventName: str):
    lookup = _get_file()
    col_name = column_name('ecoinventName')

    def emission(index: int):
        id = get_table_value(
            lookup, col_name, ecoinventName, column_name(f"emissionsResourceUse.{index}.term.id")
        )
        value = get_table_value(
            lookup, col_name, ecoinventName, column_name(f"emissionsResourceUse.{index}.value")
        )
        return (id, value) if id else None

    return non_empty_list(map(emission, range(0, 12)))
