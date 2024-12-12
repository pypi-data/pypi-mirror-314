import os
from unittest.mock import patch, call
import json
from tests.utils import fixtures_path

from hestia_earth.models.cache_sites import run

class_path = 'hestia_earth.models.cache_sites'
fixtures_folder = os.path.join(fixtures_path, 'cache_sites')
coordinates = [{"latitude": 46.47, "longitude": 2.94}]


@patch(f"{class_path}._run_query")
def test_run(mock_run_query, *args):
    with open(f"{fixtures_folder}/data.json", encoding='utf-8') as f:
        data = json.load(f)
    with open(f"{fixtures_folder}/cache.json", encoding='utf-8') as f:
        cache = json.load(f)
    with open(f"{fixtures_folder}/params.json", encoding='utf-8') as f:
        params = json.load(f)

    mock_run_query.return_value = [10] * len(params.get('rasters', []) + params.get('vectors', []))

    sites = run(data.get('nodes', []), [2019, 2020], include_region=False)

    mock_run_query.assert_has_calls([
        call({
            "ee_type": "raster",
            "collections": params.get('rasters', []),
            "coordinates": coordinates
        }),
        call({
            "ee_type": "vector",
            "collections": params.get('vectors', []),
            "coordinates": coordinates
        })
    ])

    expected = [site | {'_cache': cache} for site in data.get('nodes', [])]
    assert sites == expected


@patch(f"{class_path}._run_query")
def test_run_include_region(mock_run_query, *args):
    with open(f"{fixtures_folder}/data.json", encoding='utf-8') as f:
        data = json.load(f)
    with open(f"{fixtures_folder}/params.json", encoding='utf-8') as f:
        params = json.load(f)

    mock_run_query.return_value = [10] * len(params.get('rasters', []) + params.get('vectors', []))

    run(data.get('nodes', []), [2019, 2020], include_region=True)

    mock_run_query.assert_has_calls([
        call({
            "ee_type": "raster",
            "collections": params.get('rasters', []),
            "coordinates": coordinates
        }),
        call({
            "ee_type": "vector",
            "collections": params.get('vectors-with-regions', []),
            "coordinates": coordinates
        })
    ])
