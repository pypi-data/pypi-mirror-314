"""
Emission not relevant

The emission is not relevant for this Site, Cycle, or Product.
"""
from hestia_earth.schema import NodeType, TermTermType, EmissionMethodTier
from hestia_earth.utils.emission import emission_is_in_system_boundary

from hestia_earth.models.log import logRequirements, logShouldRun
from hestia_earth.models.utils.emission import _new_emission
from hestia_earth.models.utils.blank_node import _run_required
from hestia_earth.models.utils.term import get_all_emission_terms

REQUIREMENTS = {
    "Cycle": {
        "emissions": [{"@type": "Emission"}]
    }
}
RETURNS = {
    "Emission": [{
        "value": "0",
        "methodTier": "not relevant"
    }]
}
LOOKUPS = {
    "emission": "inHestiaDefaultSystemBoundary"
}
MODEL = 'emissionNotRelevant'
TIER = EmissionMethodTier.NOT_RELEVANT.value


def _emission(term_id: str):
    emission = _new_emission(term_id, MODEL)
    emission['value'] = [0]
    emission['methodTier'] = TIER
    return emission


def _should_run_emission(cycle: dict):
    def run(term_id: str):
        is_not_relevant = not _run_required(MODEL, {'@id': term_id, 'termType': TermTermType.EMISSION.value}, cycle)
        in_system_boundary = emission_is_in_system_boundary(term_id)

        should_run = all([is_not_relevant, in_system_boundary])
        if should_run:
            # no need to show the model failed
            logRequirements(cycle, model=MODEL, term=term_id,
                            is_not_relevant=is_not_relevant,
                            in_system_boundary=in_system_boundary,
                            run_required=False)
            logShouldRun(cycle, MODEL, term_id, should_run)
        return should_run
    return run


def _run(cycle: dict):
    emissions = get_all_emission_terms()
    term_ids = list(filter(_should_run_emission(cycle), emissions))
    return list(map(_emission, term_ids))


def _should_run(node: dict):
    node_type = node.get('@type', node.get('type'))

    logRequirements(node, model=MODEL,
                    node_type=node_type)

    should_run = node_type == NodeType.CYCLE.value
    logShouldRun(node, MODEL, None, should_run)
    return should_run


def run(_, node: dict): return _run(node) if _should_run(node) else []
