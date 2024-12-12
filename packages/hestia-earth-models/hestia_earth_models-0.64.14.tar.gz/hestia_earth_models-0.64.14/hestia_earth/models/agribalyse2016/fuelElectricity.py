"""
Fuel and Electricity

This model calculates fuel and electricity data from the number of hours each machine is operated for using.
"""
from functools import reduce
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import flatten, list_sum, non_empty_list

from hestia_earth.models.log import debugValues, logRequirements, logShouldRun, log_as_table
from hestia_earth.models.utils.term import get_lookup_value
from hestia_earth.models.utils.input import _new_input
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "completeness.electricityFuel": "False",
        "practices": [{
            "@type": "Practice",
            "term.termType": "operation",
            "value": "> 0"
        }]
    }
}
LOOKUPS = {
    "operation": "fuelUse"
}
RETURNS = {
    "Input": [{
        "term.termType": "fuel",
        "value": "",
        "operation": ""
    }]
}
MODEL_KEY = 'fuelElectricity'


def _input(term_id: str, value: float, operation: dict):
    input = _new_input(term_id, MODEL)
    input['value'] = [value]
    input['operation'] = operation
    return input


def _operation_input(operation: dict):
    input = operation.get('input', {})
    return _input(input.get('id'), input.get('value') * operation.get('value'), operation.get('term', {}))


def _run_operation(cycle: dict):
    def exec(operations: list):
        input_term_id = operations[0].get('input').get('id')
        values_logs = log_as_table([
            {
                'id': p.get('term').get('@id'),
                'value': p.get('value'),
                'coefficient': p.get('input').get('value')
            } for p in operations
        ])

        debugValues(cycle, model=MODEL, term=input_term_id,
                    values=values_logs)

        logShouldRun(cycle, MODEL, input_term_id, True, model_key=MODEL_KEY)

        return list(map(_operation_input, operations))
    return exec


def _group_operations(operations: list):
    def grouper(group: dict, operation: dict):
        input_term_id = operation.get('input').get('id')
        group[input_term_id] = group.get(input_term_id, [])
        group[input_term_id].append(operation)
        return group

    return reduce(grouper, operations, {})


def _should_run_operation(cycle: dict):
    def exec(practice: dict):
        term = practice.get('term', {})
        term_id = term.get('@id')
        values = practice.get('value', [])
        value = list_sum(values) if all([not isinstance(v, str) for v in values]) else 0  # str allowed for Practice
        has_value = value > 0

        coeffs = get_lookup_value(term, LOOKUPS['operation'], model=MODEL, model_key=MODEL_KEY)
        values = non_empty_list(coeffs.split(';')) if coeffs else []
        inputs = [{'id': c.split(':')[0], 'value': float(c.split(':')[1])} for c in values]
        has_lookup_value = len(inputs) > 0

        logRequirements(cycle, model=MODEL, term=term_id, model_key=MODEL_KEY,
                        has_value=has_value,
                        has_fuelUse_lookup_value=has_lookup_value)

        should_run = all([has_value, has_lookup_value])
        logShouldRun(cycle, MODEL, term_id, should_run, model_key=MODEL_KEY)
        return [{'term': term, 'value': value, 'input': input} for input in inputs] if should_run else []
    return exec


def _should_run(cycle: dict):
    is_incomplete = not cycle.get('completeness', {}).get('electricityFuel', False)
    operations = filter_list_term_type(cycle.get('practices', []), TermTermType.OPERATION)
    operations = flatten(map(_should_run_operation(cycle), operations))
    has_operations = len(operations) > 0

    logRequirements(cycle, model=MODEL, model_key=MODEL_KEY,
                    is_incomplete=is_incomplete,
                    has_operations=has_operations,
                    operations=';'.join(non_empty_list(map(lambda v: v.get('term', {}).get('@id'), operations))))

    should_run = all([is_incomplete, has_operations])
    logShouldRun(cycle, MODEL, None, should_run, model_key=MODEL_KEY)
    return should_run, operations


def run(cycle: dict):
    should_run, operations = _should_run(cycle)
    # group operations by input to show logs as table
    grouped_operations = _group_operations(operations)
    return flatten(map(_run_operation(cycle), grouped_operations.values())) if should_run else []
