from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.model import linked_node

from . import _term_id, _include_methodModel


def _new_indicator(term, model=None, land_cover_id=None):
    node = {'@type': SchemaType.INDICATOR.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    if land_cover_id:
        node['landCover'] = linked_node(download_hestia(land_cover_id))
    return _include_methodModel(node, model)
