"""
Excreta (kg VS)

This model calculates the Excreta (kg VS) from the products as described in
[Poore & Nemecek (2018)](https://science.sciencemag.org/content/360/6392/987).
The model computes it as the balance between the carbon in the inputs plus the carbon produced in the pond
minus the carbon contained in the primary product.
If the mass balance fails
(i.e. [animal feed](https://hestia.earth/schema/Completeness#animalFeed) is not complete, see requirements below),
the fomula is = total excreta as N / [Volatile solids content](https://hestia.earth/term/volatileSolidsContent).
"""
from hestia_earth.schema import SiteSiteType
from hestia_earth.utils.model import find_primary_product, find_term_match
from hestia_earth.utils.tools import list_sum, safe_parse_float

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.property import get_node_property
from hestia_earth.models.utils.product import _new_product
from hestia_earth.models.utils.input import get_feed_inputs
from hestia_earth.models.utils.measurement import most_relevant_measurement_value
from hestia_earth.models.utils.blank_node import convert_to_carbon
from .utils import get_excreta_product
from .excretaKgN import _get_excreta_product as get_excreta_n_product
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "products": [{
            "@type": "Product",
            "primary": "True",
            "value": "",
            "term.termType": ["animalProduct", "liveAnimal", "liveAquaticSpecies"]
        }],
        "or": [
            {
                "completeness.animalFeed": "",
                "completeness.product": "",
                "or": [
                    {
                        "animals": [{
                            "@type": "Animal",
                            "inputs": [{
                                "@type": "Input",
                                "term.units": "kg",
                                "value": "> 0",
                                "properties": [
                                    {"@type": "Property", "value": "", "term.@id": "energyContentHigherHeatingValue"},
                                    {"@type": "Property", "value": "", "term.@id": "carbonContent"}
                                ]
                            }]
                        }]
                    },
                    {
                        "inputs": [{
                            "@type": "Input",
                            "term.units": "kg",
                            "value": "> 0",
                            "isAnimalFeed": "True",
                            "properties": [
                                {"@type": "Property", "value": "", "term.@id": "energyContentHigherHeatingValue"},
                                {"@type": "Property", "value": "", "term.@id": "carbonContent"}
                            ]
                        }]
                    }
                ],
                "products": [{
                    "@type": "Product",
                    "primary": "True",
                    "value": "",
                    "properties": [{"@type": "Property", "value": "", "term.@id": "carbonContent"}]
                }],
                "practices": [
                    {"@type": "Practice", "value": "", "term.@id": "slaughterAge"},
                    {"@type": "Practice", "value": "", "term.@id": "yieldOfPrimaryAquacultureProductLiveweightPerM2"}
                ],
                "site": {
                    "@type": "Site",
                    "measurements": [{"@type": "Measurement", "value": "", "term.@id": "netPrimaryProduction"}]
                }
            }
        ]
    }
}
RETURNS = {
    "Product": [{
        "value": ""
    }]
}
LOOKUPS = {
    "crop-property": ["carbonContent", "energyContentHigherHeatingValue"],
    "animalProduct": ["excretaKgVsTermIds", "allowedExcretaKgVsTermIds"],
    "liveAnimal": ["excretaKgVsTermIds", "allowedExcretaKgVsTermIds"],
    "liveAquaticSpecies": ["excretaKgVsTermIds", "allowedExcretaKgVsTermIds"]
}
MODEL_KEY = 'excretaKgVs'

Conv_AQ_CLW_CO2CR = 1
Conv_AQ_CLW_CExcr = 0.5
Conv_AQ_OC_OCSed_Marine = 0.55
Conv_AQ_OC_OCSed_Fresh = 0.35


def _product(excreta_product: str, value: float):
    product = _new_product(excreta_product.get('term', {}).get('@id'), value, MODEL)
    return excreta_product | product


def _run(excreta_product: dict, mass_balance_items: list, inputs_c: float, alternate_items: list):
    carbonContent, tsy, slaughterAge, aqocsed, npp = mass_balance_items
    excretaKgN, vsc = alternate_items
    value = max(
        inputs_c + (npp * slaughterAge) / (tsy * 1000) - carbonContent - carbonContent * Conv_AQ_CLW_CO2CR,
        carbonContent * Conv_AQ_CLW_CExcr
    ) * aqocsed if all(mass_balance_items) else excretaKgN * vsc / 100
    return [_product(excreta_product, value)] if value > 0 else []


def _get_carbonContent(cycle: dict):
    primary_prod = find_primary_product(cycle) or {}
    return safe_parse_float(
        get_lookup_value(primary_prod.get('term', {}), 'carbonContent', model=MODEL, model_key=MODEL_KEY)
    ) / 100


def _get_conv_aq_ocsed(siteType: str):
    return Conv_AQ_OC_OCSed_Marine if siteType == SiteSiteType.SEA_OR_OCEAN.value else Conv_AQ_OC_OCSed_Fresh


def _get_excreta_product(cycle: dict, primary_product: dict):
    term = primary_product.get('term', {})
    return get_excreta_product(cycle, term, 'excretaKgVsTermIds', 'allowedExcretaKgVsTermIds')


def _should_run(cycle: dict):
    primary_prod = find_primary_product(cycle) or {}
    excreta_product = _get_excreta_product(cycle, primary_prod)
    excreta_term_id = excreta_product.get('term', {}).get('@id')
    should_add_product = all([not excreta_product.get('value', [])])

    dc = cycle.get('completeness', {})
    is_animalFeed_complete = dc.get('animalFeed', False)
    is_product_complete = dc.get('product', False)

    carbonContent = _get_carbonContent(cycle)

    inputs_feed = get_feed_inputs(cycle)
    inputs_c = convert_to_carbon(cycle, MODEL, excreta_term_id, inputs_feed, model_key=MODEL_KEY)

    practices = cycle.get('practices', [])
    tsy = list_sum(find_term_match(practices, 'yieldOfPrimaryAquacultureProductLiveweightPerM2').get('value', []))
    slaughterAge = list_sum(find_term_match(practices, 'slaughterAge').get('value', []))

    end_date = cycle.get('endDate')
    site = cycle.get('site', {})
    aqocsed = _get_conv_aq_ocsed(site.get('siteType', {}))
    npp = most_relevant_measurement_value(site.get('measurements', []), 'netPrimaryProduction', end_date, 0)

    # we can still run the model with excreta in "kg N" units
    excreta_n_product = get_excreta_n_product(cycle, primary_prod)
    excretaKgN = list_sum(excreta_n_product.get('value', [0]))
    vsc = get_node_property(excreta_n_product, 'volatileSolidsContent').get('value', 0)

    logRequirements(cycle, model=MODEL, term=excreta_term_id, model_key=MODEL_KEY,
                    is_animalFeed_complete=is_animalFeed_complete,
                    is_product_complete=is_product_complete,
                    aqocsed=aqocsed,
                    inputs_c=inputs_c,
                    carbonContent=carbonContent,
                    yield_of_target_species=tsy,
                    slaughterAge=slaughterAge,
                    netPrimaryProduction=npp,
                    excretaKgN=excretaKgN,
                    volatileSolidsContent=vsc)

    mass_balance_items = [carbonContent, tsy, slaughterAge, aqocsed, npp]
    alternate_items = [excretaKgN, vsc]

    should_run = all([
        excreta_term_id,
        should_add_product,
        any([
            is_animalFeed_complete and is_product_complete and all(mass_balance_items),
            all(alternate_items)
        ])
    ])
    # only log if the excreta term does not exist to avoid showing failure when it already exists
    if should_add_product:
        logShouldRun(cycle, MODEL, excreta_term_id, should_run, model_key=MODEL_KEY)
    logShouldRun(cycle, MODEL, None, should_run)
    return should_run, excreta_product, mass_balance_items, inputs_c, alternate_items


def run(cycle: dict):
    should_run, excreta_product, mass_balance_items, inputs_c, alternate_items = _should_run(cycle)
    return _run(excreta_product, mass_balance_items, inputs_c, alternate_items) if should_run else []
