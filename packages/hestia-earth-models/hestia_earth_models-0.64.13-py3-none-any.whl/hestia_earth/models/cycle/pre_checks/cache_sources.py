"""
Pre Checks Cache Sources

This model caches the sources of all models.
"""
from hestia_earth.models.log import debugValues
from hestia_earth.models.utils import CACHE_KEY, cached_value
from hestia_earth.models.utils.source import CACHE_SOURCES_KEY, find_sources

REQUIREMENTS = {
    "Cycle": {}
}
RETURNS = {
    "Cycle": {}
}


def _should_run(site: dict):
    sources = find_sources()
    has_cache = cached_value(site, CACHE_SOURCES_KEY) is not None

    debugValues(site,
                sources=';'.join([str(title) for title in sources.keys()]),
                has_cache=has_cache)

    should_run = all([
        not has_cache,
        len(sources) > 0
    ])
    return should_run, sources


def run(site: dict):
    should_run, sources = _should_run(site)
    return {
        **site,
        CACHE_KEY: cached_value(site) | {CACHE_SOURCES_KEY: sources}
    } if should_run else site
