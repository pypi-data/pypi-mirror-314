from unittest.mock import patch

from hestia_earth.models.site.pre_checks.cache_sources import CACHE_KEY, CACHE_SOURCES_KEY, run, _should_run

class_path = 'hestia_earth.models.site.pre_checks.cache_sources'
sources = {'source a': {'@type': 'Source', '@id': 'source-1'}}


def test_should_run():
    # no existing cache => run
    assert _should_run({CACHE_KEY: {}}) is True
    assert _should_run({CACHE_KEY: {CACHE_SOURCES_KEY: {}}}) is True

    # with existing cache => no run
    assert not _should_run({CACHE_KEY: {CACHE_SOURCES_KEY: {'sample': 'a'}}})


@patch(f"{class_path}.find_sources", return_value=sources)
def test_run(*args):
    result = run({})
    assert result.get(CACHE_KEY).get(CACHE_SOURCES_KEY) == sources
