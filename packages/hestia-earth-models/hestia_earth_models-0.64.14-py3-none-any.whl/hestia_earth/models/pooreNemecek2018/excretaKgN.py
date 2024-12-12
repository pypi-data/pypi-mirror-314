"""
Excreta (kg N)

This model uses a mass balance to calculate the total amount of excreta (as N) created by animals.
The inputs into the mass balance are the total amount of feed and the total amount of net primary production
in the water body.
The outputs of the mass balance are the weight of the animal and the excreta.
The formula is excreta = feed + NPP - animal.

For [live aquatic species](https://hestia.earth/glossary?termType=liveAquaticSpecies), if the mass balance fails
(i.e. [animal feed](https://hestia.earth/schema/Completeness#animalFeed) is not complete, see requirements below),
a simplified formula is used: total nitrogen content of the fish * 3.31.
See [Poore & Nemecek (2018)](https://science.sciencemag.org/content/360/6392/987) for further details.
"""
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.property import _get_nitrogen_content
from hestia_earth.models.utils.input import get_feed_inputs
from hestia_earth.models.utils.product import _new_product, get_animal_produced_nitrogen
from hestia_earth.models.utils.blank_node import convert_to_nitrogen
from .utils import get_excreta_product
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "completeness.animalFeed": "",
        "completeness.product": "",
        "products": [{
            "@type": "Product",
            "value": "",
            "term.termType": ["liveAnimal", "animalProduct", "liveAquaticSpecies"],
            "optional": {
                "properties": [{"@type": "Property", "value": "", "term.@id": "nitrogenContent"}]
            }
        }],
        "or": [
            {
                "animals": [{
                    "@type": "Animal",
                    "inputs": [{
                        "@type": "Input",
                        "term.units": "kg",
                        "value": "> 0",
                        "properties": [
                            {"@type": "Property", "value": "", "term.@id": "nitrogenContent"},
                            {"@type": "Property", "value": "", "term.@id": "crudeProteinContent"}
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
                        {"@type": "Property", "value": "", "term.@id": "nitrogenContent"},
                        {"@type": "Property", "value": "", "term.@id": "crudeProteinContent"}
                    ]
                }]
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
    "crop-property": ["nitrogenContent", "crudeProteinContent"],
    "animalProduct": ["excretaKgNTermIds", "allowedExcretaKgNTermIds"],
    "liveAnimal": ["excretaKgNTermIds", "allowedExcretaKgNTermIds"],
    "liveAquaticSpecies": ["excretaKgNTermIds", "allowedExcretaKgNTermIds"]
}
MODEL_KEY = 'excretaKgN'


def _product(excreta_product: str, value: float):
    product = _new_product(excreta_product.get('term', {}).get('@id'), value, MODEL)
    return excreta_product | product


def _run(excreta_product: dict, mass_balance_items: list, alternate_items: list):
    inputs_n, products_n = mass_balance_items
    product_value, nitrogen_content = alternate_items
    value = inputs_n - products_n if all(mass_balance_items) else 3.31 * product_value * nitrogen_content / 100
    return [_product(excreta_product, value)] if value > 0 else []


def _get_excreta_product(cycle: dict, primary_product: dict):
    term = primary_product.get('term', {})
    return get_excreta_product(cycle, term, 'excretaKgNTermIds', 'allowedExcretaKgNTermIds')


def _should_run(cycle: dict):
    primary_prod = find_primary_product(cycle) or {}
    excreta_product = _get_excreta_product(cycle, primary_prod)
    excreta_term_id = excreta_product.get('term', {}).get('@id')
    should_add_product = all([not excreta_product.get('value', [])])

    dc = cycle.get('completeness', {})
    is_animalFeed_complete = dc.get('animalFeed', False)
    is_product_complete = dc.get('product', False)

    inputs_feed = get_feed_inputs(cycle)
    inputs_n = convert_to_nitrogen(cycle, MODEL, excreta_term_id, inputs_feed, model_key=MODEL_KEY)

    products_n = get_animal_produced_nitrogen(MODEL, cycle.get('products', []))

    # we can still run the model for `liveAquaticSpecies`
    is_liveAquaticSpecies = primary_prod.get('term', {}).get('termType') == TermTermType.LIVEAQUATICSPECIES.value
    product_value = list_sum(primary_prod.get('value', [0]))
    nitrogen_content = _get_nitrogen_content(primary_prod)

    if is_liveAquaticSpecies:
        logRequirements(cycle, model=MODEL, term=excreta_term_id, model_key=MODEL_KEY,
                        is_liveAquaticSpecies=is_liveAquaticSpecies,
                        product_value=product_value,
                        nitrogen_content=nitrogen_content)

    else:
        logRequirements(cycle, model=MODEL, term=excreta_term_id, model_key=MODEL_KEY,
                        is_animalFeed_complete=is_animalFeed_complete,
                        is_product_complete=is_product_complete,
                        inputs_n=inputs_n,
                        products_n=products_n)

    mass_balance_items = [inputs_n, products_n]
    alternate_items = [product_value, nitrogen_content]

    should_run = all([
        excreta_term_id,
        should_add_product,
        any([
            is_animalFeed_complete and is_product_complete and all(mass_balance_items),
            is_liveAquaticSpecies and all(alternate_items)
        ])
    ])
    # only log if the excreta term does not exist to avoid showing failure when it already exists
    if should_add_product:
        logShouldRun(cycle, MODEL, excreta_term_id, should_run, model_key=MODEL_KEY)
    logShouldRun(cycle, MODEL, None, should_run)
    return should_run, excreta_product, mass_balance_items, alternate_items


def run(cycle: dict):
    should_run, excreta_product, mass_balance_items, alternate_items = _should_run(cycle)
    return _run(excreta_product, mass_balance_items, alternate_items) if should_run else []
