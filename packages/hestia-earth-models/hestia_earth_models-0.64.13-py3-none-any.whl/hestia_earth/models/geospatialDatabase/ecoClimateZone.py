"""
They approximataely map to the [IPCC (2019) Climate Zones](https://www.ipcc-nggip.iges.or.jp/public/2019rf/pdf/4_Volume4/19R_V4_Ch03_Land%20Representation.pdf).  # noqa: E501
Data are derived from [Hiederer et al. (2010) Biofuels: A new methodology to estimate GHG emissions from global land use change, European Commission Joint Research Centre](https://ec.europa.eu/jrc/en/publication/eur-scientific-and-technical-research-reports/biofuels-new-methodology-estimate-ghg-emissions-due-global-land-use-change-methodology).  # noqa: E501

| Value | Climate Zone         |
|-------|----------------------|
| 1     | Warm Temperate Moist |
| 2     | Warm Temperate Dry   |
| 3     | Cool Temperate Moist |
| 4     | Cool Temperate Dry   |
| 5     | Polar Moist          |
| 6     | Polar Dry            |
| 7     | Boreal Moist         |
| 8     | Boreal Dry           |
| 9     | Tropical Montane     |
| 10    | Tropical Wet         |
| 11    | Tropical Moist       |
| 12    | Tropical Dry         |
"""
from hestia_earth.schema import MeasurementMethodClassification
from hestia_earth.utils.lookup import download_lookup, _get_single_table_value, column_name

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.measurement import _new_measurement
from hestia_earth.models.utils.source import get_source
from .utils import download, get_region_factor, has_geospatial_data, should_download
from . import MODEL

REQUIREMENTS = {
    "Site": {
        "or": [
            {"latitude": "", "longitude": ""},
            {"boundary": {}},
            {"region": {"@type": "Term", "termType": "region"}}
        ]
    }
}
RETURNS = {
    "Measurement": [{
        "value": "",
        "description": "",
        "methodClassification": "geospatial dataset"
    }]
}
LOOKUPS = {
    "region-measurment": "ecoClimateZone"
}
TERM_ID = 'ecoClimateZone'
EE_PARAMS = {
    'collection': 'climate_zone',
    'ee_type': 'raster',
    'reducer': 'mode'
}
BIBLIO_TITLE = 'Biofuels: A new methodology to estimate GHG emissions from global land use change'


def _measurement(site: dict, value: int):
    measurement = _new_measurement(TERM_ID)
    measurement['description'] = _name(value)
    measurement['value'] = [value]
    measurement['methodClassification'] = MeasurementMethodClassification.GEOSPATIAL_DATASET.value
    return measurement | get_source(site, BIBLIO_TITLE)


def _name(value: int):
    lookup = download_lookup(f"{TERM_ID}.csv")
    return _get_single_table_value(lookup, column_name(TERM_ID), value, 'name')


def _run(site: dict):
    value = download(TERM_ID, site, EE_PARAMS)
    return [_measurement(site, round(value))] if value is not None else []


def _run_default(site: dict):
    region_factor = get_region_factor(TERM_ID, site)

    logRequirements(site, model=MODEL, term=TERM_ID,
                    region_factor=region_factor)

    should_run = all([region_factor])
    logShouldRun(site, MODEL, TERM_ID, should_run)
    return [_measurement(site, round(region_factor))] if should_run else []


def _should_run(site: dict):
    contains_geospatial_data = has_geospatial_data(site)
    below_max_area_size = should_download(TERM_ID, site)

    logRequirements(site, model=MODEL, term=TERM_ID,
                    contains_geospatial_data=contains_geospatial_data,
                    below_max_area_size=below_max_area_size)

    should_run = all([contains_geospatial_data, below_max_area_size])
    logShouldRun(site, MODEL, TERM_ID, should_run)
    return should_run


def run(site: dict): return _run(site) if _should_run(site) else _run_default(site)
