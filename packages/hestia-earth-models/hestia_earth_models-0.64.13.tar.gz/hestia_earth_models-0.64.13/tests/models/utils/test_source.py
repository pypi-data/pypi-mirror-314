from unittest.mock import patch

from hestia_earth.models.utils.source import _list_sources, find_sources

class_path = 'hestia_earth.models.utils.source'
search_results = [{
    '@type': 'Source',
    '@id': 'source-1',
    'name': 'Source 1',
    'bibliography': {'title': 'Biblio 1'}
}]


def test_list_sources():
    assert len(_list_sources()) == 10


@patch(f"{class_path}.search", return_value=search_results)
def test_find_sources(*args):
    sources = find_sources()
    assert sources == {
        'Biblio 1': {
            '@type': 'Source',
            '@id': 'source-1',
            'name': 'Source 1'
        }
    }
