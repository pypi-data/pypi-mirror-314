from unittest.mock import patch

from hestia_earth.models.cycle.pre_checks.cache_sources import CACHE_KEY, CACHE_SOURCES_KEY, run, _should_run

class_path = 'hestia_earth.models.cycle.pre_checks.cache_sources'
sources = {'source a': {'@type': 'Source', '@id': 'source-1'}}


@patch(f"{class_path}.find_sources")
def test_should_run(mock_find_sources):
    # no sources => no run
    mock_find_sources.return_value = {}
    should_run, *args = _should_run({})
    assert not should_run

    # with sources => run
    mock_find_sources.return_value = sources
    should_run, *args = _should_run({})
    assert should_run is True


@patch(f"{class_path}.find_sources", return_value=sources)
def test_run(*args):
    result = run({})
    assert result.get(CACHE_KEY).get(CACHE_SOURCES_KEY) == sources
