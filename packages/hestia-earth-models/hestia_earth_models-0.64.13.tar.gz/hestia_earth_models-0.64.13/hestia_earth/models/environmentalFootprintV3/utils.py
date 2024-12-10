from typing import Optional
from hestia_earth.utils.lookup import download_lookup
from hestia_earth.utils.lookup import get_table_value, column_name

from hestia_earth.models.log import debugMissingLookup
from . import MODEL


def get_coefficient_factor(lookup_name: str, country_id: str, occupation_type: Optional[str], term_id: str):
    """
    Gets the EU PEF Characteristic factor for a given eu site type and country
    """
    coefficient = get_table_value(download_lookup(lookup_name), 'termid', country_id, column_name(occupation_type))
    debugMissingLookup(
        lookup_name, 'termid', country_id, occupation_type, coefficient, model=MODEL, term=term_id
    )
    return coefficient
