import json
from unittest.mock import patch
from tests.utils import fixtures_path

from hestia_earth.models.faostat2018.product.price import MODEL, MODEL_KEY, run, _lookup_data

class_path = f"hestia_earth.models.{MODEL}.product.{MODEL_KEY}"
fixtures_folder = f"{fixtures_path}/{MODEL}/product/{MODEL_KEY}"


def test_lookup_data():
    assert _lookup_data('cocoaSeedDehulled', 'Cocoa beans', 'GADM-GHA', 2000, term_type='crop') == 412.9
    # average price per tonne as year value is missing
    assert _lookup_data('cocoaSeedDehulled', 'Cocoa beans', 'GADM-GHA', 2012, term_type='crop') == 843.5571428571428


@patch(f"{class_path}.download_hestia", return_value={})
def test_run_crop(*args):
    with open(f"{fixtures_folder}/crop/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/crop/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


@patch(f"{class_path}.download_hestia", return_value={})
def test_run_animalProduct_kg(*args):
    with open(f"{fixtures_folder}/animalProduct/kg/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/animalProduct/kg/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


@patch(f"{class_path}.download_hestia", return_value={})
def test_run_animalProduct_number(*args):
    with open(f"{fixtures_folder}/animalProduct/number/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/animalProduct/number/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    value = run(cycle)
    assert value == expected


@patch(f"{class_path}.download_hestia")
def test_run_liveAnimal_chicken(mock_download_hestia):
    with open(f"{fixtures_folder}/liveAnimal/chicken/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/liveAnimal/chicken/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    mock_download_hestia.return_value = {
        "@id": "meatChickenLiveweight",
        "@type": "Term",
        "units": "kg liveweight",
        "termType": "animalProduct"
    }
    value = run(cycle)
    assert value == expected


@patch(f"{class_path}.download_hestia")
def test_run_liveAnimal_pig(mock_download_hestia):
    with open(f"{fixtures_folder}/liveAnimal/pig/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/liveAnimal/pig/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    mock_download_hestia.return_value = {
        "@id": "meatPigLiveweight",
        "@type": "Term",
        "units": "kg liveweight",
        "termType": "animalProduct"
    }
    value = run(cycle)
    assert value == expected


@patch(f"{class_path}.download_hestia")
def test_run_liveAnimal_sheepLamb(mock_download_hestia):
    with open(f"{fixtures_folder}/liveAnimal/sheepLamb/cycle.jsonld", encoding='utf-8') as f:
        cycle = json.load(f)

    with open(f"{fixtures_folder}/liveAnimal/sheepLamb/result.jsonld", encoding='utf-8') as f:
        expected = json.load(f)

    mock_download_hestia.return_value = {
        "@id": "meatSheepLiveweight",
        "@type": "Term",
        "units": "kg liveweight",
        "termType": "animalProduct"
    }
    value = run(cycle)
    assert value == expected
