"""
Characterises [soilQualityIndexTotalLandUseEffects](https://hestia.earth/term/soilQualityIndexTotalLandUseEffects)
based on an updated [LANCA model (De Laurentiis et al. 2019)](
http://publications.jrc.ec.europa.eu/repository/handle/JRC113865) and on the LANCA (Regionalised) Characterisation
Factors version 2.5 (Horn and Meier, 2018).
"""
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun
from . import MODEL
from ..utils.indicator import _new_indicator

REQUIREMENTS = {
    "ImpactAssessment": {
        "emissionsResourceUse": [
            {"@type": "Indicator", "value": "", "term.@id": "soilQualityIndexLandOccupation"},
            {"@type": "Indicator", "value": "", "term.@id": "soilQualityIndexLandTransformation"}
        ]
    }
}

RETURNS = {
    "Indicator": {
        "value": "",
        "methodTier": "tier 1",
        "statsDefinition": "modelled"
    }
}
TERM_ID = 'soilQualityIndexTotalLandUseEffects'


def _indicator(value: float):
    indicator = _new_indicator(TERM_ID, MODEL)
    indicator['value'] = value
    return indicator


def _run(indicators: list):
    values = [indicator['value'] for indicator in indicators]
    return _indicator(list_sum(values))


def _should_run(impactassessment: dict) -> tuple[bool, list]:
    land_indicators = [
        i for i in impactassessment.get('emissionsResourceUse', []) if
        i.get('term', {}).get('@id', '') in ['soilQualityIndexLandOccupation', 'soilQualityIndexLandTransformation']
    ]
    has_indicators = bool(land_indicators)

    land_occupation_indicator = find_term_match(land_indicators, "soilQualityIndexLandOccupation",
                                                default_val=None)
    has_land_occupation_indicator = bool(land_occupation_indicator)

    land_transformation_indicator = find_term_match(land_indicators, "soilQualityIndexLandTransformation",
                                                    default_val=None)
    has_land_transformation_indicator = bool(land_transformation_indicator)

    has_valid_values = all([isinstance(indicator.get('value', None), (int, float)) for indicator in land_indicators])

    logRequirements(impactassessment, model=MODEL, term=TERM_ID,
                    has_indicators=has_indicators,
                    has_land_occupation_indicator=has_land_occupation_indicator,
                    has_land_transformation_indicator=has_land_transformation_indicator,
                    has_valid_values=has_valid_values
                    )

    should_run = all([has_indicators, has_valid_values,
                      has_land_occupation_indicator, has_land_transformation_indicator])

    logShouldRun(impactassessment, MODEL, TERM_ID, should_run)
    return should_run, land_indicators


def run(impactassessment: dict):
    should_run, indicators = _should_run(impactassessment)
    return _run(indicators) if should_run else None
