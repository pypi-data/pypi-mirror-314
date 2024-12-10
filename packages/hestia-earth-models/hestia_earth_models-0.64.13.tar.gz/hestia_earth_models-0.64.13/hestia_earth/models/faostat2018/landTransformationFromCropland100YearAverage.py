from hestia_earth.utils.model import find_term_match

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_country_id, impact_end_year
from . import MODEL
from .utils import get_cropland_ratio

REQUIREMENTS = {
    "ImpactAssessment": {
        "endDate": "",
        "country": {"@type": "Term", "termType": "region"},
        "emissionsResourceUse": [
            {"@type": "Indicator", "value": "", "term.@id": "landTransformationFromCropland100YearAverageDuringCycle"}
        ]
    }
}
LOOKUPS = {
    "region-faostatArea": ""
}
RETURNS = {
    "Indicator": [{
        "value": "",
        "landCover": ""
    }]
}
TERM_ID = 'landTransformationFromTemporaryCropland100YearAverageDuringCycle,landTransformationFromPermanentCropland100YearAverageDuringCycle'  # noqa: E501
FROM_TERM_ID = 'landTransformationFromCropland100YearAverageDuringCycle'
TEMPORARY_TERM_ID = 'landTransformationFromTemporaryCropland100YearAverageDuringCycle'
PERMANENT_TERM_ID = 'landTransformationFromPermanentCropland100YearAverageDuringCycle'


def _indicator(term_id: str, value: float):
    indicator = _new_indicator(term_id, MODEL, 'cropland')
    indicator['value'] = value
    return indicator


def _run(impact: dict, value: float):
    country_id = get_country_id(impact)
    end_year = impact_end_year(impact)
    total, permanent, temporary = get_cropland_ratio(country_id, end_year - 100, end_year)

    debugValues(impact, model=MODEL, term_id=TEMPORARY_TERM_ID,
                diff_temporary_area=temporary,
                diff_total_area=total)
    debugValues(impact, model=MODEL, term_id=PERMANENT_TERM_ID,
                diff_permanent_area=permanent,
                diff_total_area=total)

    return [
        _indicator(TEMPORARY_TERM_ID, value * temporary / total),
        _indicator(PERMANENT_TERM_ID, value * permanent / total)
    ] if total is not None else []


def _should_run(impact: dict):
    indicator = find_term_match(impact.get('emissionsResourceUse', []), FROM_TERM_ID)
    cropland_value = indicator.get('value', 0)
    has_cropland = cropland_value > 0

    should_run = all([has_cropland])
    for term_id in TERM_ID.split(','):
        logRequirements(impact, model=MODEL, term=term_id,
                        has_cropland=has_cropland,
                        cropland_value=cropland_value)
        logShouldRun(impact, MODEL, term_id, should_run)

    return should_run, cropland_value


def run(impact: dict):
    should_run, value = _should_run(impact)
    return _run(impact, value) if should_run else []
