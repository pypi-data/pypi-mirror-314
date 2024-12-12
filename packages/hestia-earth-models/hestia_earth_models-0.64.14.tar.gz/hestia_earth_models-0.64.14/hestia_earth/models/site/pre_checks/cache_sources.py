"""
Pre Checks Cache Sources

This model caches the sources of all Site models.
"""
from hestia_earth.models.log import debugValues
from hestia_earth.models.utils import CACHE_KEY, cached_value
from hestia_earth.models.utils.source import CACHE_SOURCES_KEY, find_sources

REQUIREMENTS = {
    "Site": {}
}
RETURNS = {
    "Site": {}
}


def _run(site: dict):
    sources = find_sources()
    debugValues(site, sources=';'.join([str(title) for title in sources.keys()]))
    return sources


def _should_run(site: dict):
    has_cache = cached_value(site, CACHE_SOURCES_KEY)
    return not bool(has_cache)


def run(site: dict):
    should_run = _should_run(site)
    return {
        **site,
        CACHE_KEY: cached_value(site) | {CACHE_SOURCES_KEY: _run(site)}
    } if should_run else site
