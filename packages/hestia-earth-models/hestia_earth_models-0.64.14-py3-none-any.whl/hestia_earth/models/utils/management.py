from hestia_earth.schema import SchemaType
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.api import download_hestia

from . import _term_id, _include_model


def _new_management(term, model=None):
    node = {'@type': SchemaType.MANAGEMENT.value}
    node['term'] = linked_node(term if isinstance(term, dict) else download_hestia(_term_id(term)))
    return _include_model(node, model)
