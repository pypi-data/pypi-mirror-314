from hestia_earth.models.log import debugValues, logRequirements, logShouldRun
from hestia_earth.models.utils.indicator import _new_indicator
from hestia_earth.models.utils.impact_assessment import get_product, get_site
from hestia_earth.models.utils.cycle import land_occupation_per_kg
from .utils import get_emission_factor
from . import MODEL

REQUIREMENTS = {
    "ImpactAssessment": {
        "product": {"@type": "Product", "term": {"@type": "Term"}},
        "site": {
            "@type": "Site",
            "siteType": ""
        },
        "cycle": {
            "@type": "Cycle",
            "products": [{
                "@type": "Product",
                "primary": "True",
                "value": "> 0",
                "economicValueShare": "> 0"
            }],
            "or": [
                {
                    "@doc": "if the [cycle.functionalUnit](https://hestia.earth/schema/Cycle#functionalUnit) = 1 ha, additional properties are required",  # noqa: E501
                    "cycleDuration": "",
                    "practices": [{"@type": "Practice", "value": "", "term.@id": "longFallowRatio"}]
                },
                {
                    "@doc": "for plantations, additional properties are required",
                    "practices": [
                        {"@type": "Practice", "value": "", "term.@id": "nurseryDensity"},
                        {"@type": "Practice", "value": "", "term.@id": "nurseryDuration"},
                        {"@type": "Practice", "value": "", "term.@id": "plantationProductiveLifespan"},
                        {"@type": "Practice", "value": "", "term.@id": "plantationDensity"},
                        {"@type": "Practice", "value": "", "term.@id": "plantationLifespan"},
                        {"@type": "Practice", "value": "", "term.@id": "rotationDuration"}
                    ]
                }
            ]
        }
    }
}
LOOKUPS = {
    "crop": "cropGroupingFaostatArea",
    "region-crop-cropGroupingFaostatArea-landTransformation20YearsAverage": "use crop grouping above or default to site.siteType"  # noqa: E501
}
RETURNS = {
    "Indicator": [{
        "value": ""
    }]
}
TERM_ID = 'landTransformationFromForest20YearAverageDuringCycle'


def _indicator(term_id: str, value: float):
    indicator = _new_indicator(term_id, MODEL)
    indicator['value'] = value
    return indicator


def _run(impact_assessment: dict, land_occupation_m2: float, factor: float):
    value = land_occupation_m2 * (factor or 0)
    debugValues(impact_assessment, model=MODEL, term=TERM_ID,
                value=value)
    return _indicator(TERM_ID, value)


def _should_run(impact_assessment: dict):
    cycle = impact_assessment.get('cycle', {})
    product = get_product(impact_assessment)
    site = get_site(impact_assessment)
    land_occupation_m2_kg = land_occupation_per_kg(MODEL, TERM_ID, cycle, site, product)
    land_transformation_factor = get_emission_factor(TERM_ID, cycle, 'landTransformation20YearsAverage')

    logRequirements(impact_assessment, model=MODEL, term=TERM_ID,
                    land_occupation_m2_kg=land_occupation_m2_kg,
                    land_transformation_factor=land_transformation_factor)

    should_run = all([
        land_occupation_m2_kg is not None,
        land_occupation_m2_kg == 0 or land_transformation_factor is not None
    ])
    logShouldRun(impact_assessment, MODEL, TERM_ID, should_run)
    return should_run, land_occupation_m2_kg, land_transformation_factor


def run(impact_assessment: dict):
    should_run, land_occupation_m2, factor = _should_run(impact_assessment)
    return [_run(impact_assessment, land_occupation_m2, factor)] if should_run else []
