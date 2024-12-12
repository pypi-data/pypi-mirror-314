from hestia_earth.schema import EmissionMethodTier, CycleFunctionalUnit

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.cycle import land_occupation_per_ha
from .utils import get_emission_factor
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "functionalUnit": "1 ha",
        "or": [
            {
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
        ],
        "site": {
            "@type": "Site",
            "country": {"@type": "Term", "termType": "region"}
        }
    }
}
LOOKUPS = {
    "crop": ["isPlantation", "cropGroupingFaostatArea"],
    "region-crop-cropGroupingFaostatArea-co2LandUseChange": "use crop grouping above or default to site.siteType"
}
RETURNS = {
    "Emission": [{
        "value": "",
        "methodTier": "tier 1"
    }]
}
TERM_ID = 'co2ToAirAboveGroundBiomassStockChangeLandUseChange'
TIER = EmissionMethodTier.TIER_1.value


def _emission(value: float):
    emission = _new_emission(TERM_ID, MODEL)
    emission['value'] = [value]
    emission['methodTier'] = TIER
    return emission


def _run(land_occupation: float, co2_land_use_change: float):
    value = land_occupation * co2_land_use_change
    return [_emission(value)]


def _should_run(cycle: dict):
    is_1_ha_functional_unit = cycle.get('functionalUnit') == CycleFunctionalUnit._1_HA.value
    land_occupation = land_occupation_per_ha(MODEL, TERM_ID, cycle)
    co2_land_use_change = get_emission_factor(TERM_ID, cycle, 'co2LandUseChange')

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    is_1_ha_functional_unit=is_1_ha_functional_unit,
                    land_occupation=land_occupation,
                    co2_land_use_change=co2_land_use_change)

    should_run = all([is_1_ha_functional_unit, land_occupation, co2_land_use_change is not None])
    logShouldRun(cycle, MODEL, TERM_ID, should_run, methodTier=TIER)
    return should_run, land_occupation, co2_land_use_change


def run(cycle: dict):
    should_run, land_occupation, co2_land_use_change = _should_run(cycle)
    return _run(land_occupation, co2_land_use_change) if should_run else []
