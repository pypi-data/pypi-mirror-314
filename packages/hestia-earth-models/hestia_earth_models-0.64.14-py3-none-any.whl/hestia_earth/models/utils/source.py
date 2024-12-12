import pathlib
from os.path import dirname, abspath, join
import re
from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import find_node_exact, search
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.tools import flatten

from . import cached_value

ROOT_DIR = abspath(join(dirname(abspath(__file__)), '..'))
CACHE_SOURCES_KEY = 'sources'


def _find_source(biblio_title: str = None):
    source = find_node_exact(SchemaType.SOURCE, {'bibliography.title': biblio_title}) if biblio_title else None
    return None if source is None else linked_node({'@type': SchemaType.SOURCE.value, **source})


def get_source(node: dict, biblio_title: str = None):
    source = cached_value(node, CACHE_SOURCES_KEY, {}).get(biblio_title) or _find_source(biblio_title)
    return {'source': source} if source else {}


def _extract(content: str):
    return [str(m) for m in re.findall(r'BIBLIO_TITLE = \'.*\'', content)]


def _clean(title: str): return title.replace("BIBLIO_TITLE = ", '').replace("'", '')


def _list_sources():
    dir = pathlib.Path(ROOT_DIR)
    files = list(dir.rglob('**/*.py'))
    sources = list(set(flatten([_extract(open(f, 'r').read()) for f in files])))
    return list(map(_clean, sources))


def find_sources():
    titles = _list_sources()
    query = {
        'bool': {
            'must': [{'match': {'@type': SchemaType.SOURCE.value}}],
            'should': [{'match': {'bibliography.title.keyword': title}} for title in titles],
            'minimum_should_match': 1
        }
    }
    results = search(query, fields=['@type', '@id', 'name', 'bibliography.title'], limit=len(titles))
    return {result.get('bibliography').get('title'): linked_node(result) for result in results}
