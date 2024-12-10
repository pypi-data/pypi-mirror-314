from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.api import download_hestia

from hestia_earth.orchestrator.log import debugValues, logShouldRun
from hestia_earth.orchestrator.utils import get_required_model_param, find_term_match

_ALLOW_ALL = 'all'


def _lookup_values(term: dict, column: str):
    term_id = term.get('@id')
    term_type = term.get('termType')
    lookup = download_lookup(f"{term_type}.csv")
    values = get_table_value(lookup, 'termid', term_id, column_name(column))
    return (values or _ALLOW_ALL).split(';')


def _is_node_type_allowed(data: dict, term_id: str):
    node_type = data.get('@type', data.get('type'))
    term = download_hestia(term_id)
    allowed_types = _lookup_values(term, 'typesAllowed') if term else [_ALLOW_ALL]
    return True if _ALLOW_ALL in allowed_types or not node_type else node_type in allowed_types


def _run_required(data: dict, model: str, term_id: str):
    node_type_allowed = _is_node_type_allowed(data, term_id)

    run_required = all([node_type_allowed])
    debugValues(data, model=model, term=term_id,
                run_required=run_required,
                node_type_allowed=node_type_allowed)
    return run_required


_RUN_FROM_ARGS = {
    'runNonAddedTerm': lambda node: 'term' not in node.get('added', []),
    'runNonMeasured': lambda node: node.get('methodTier') != 'measured'
}


def _is_empty(node: dict, skip_empty_value: bool = False):
    return node is None or all([
        not skip_empty_value,
        node.get('value') is None or node.get('value') == []
    ])


def _run_aggregated(data: dict, skip_aggregated: bool = False):
    return not data.get('aggregated', False) or not skip_aggregated


def _is_0_emission(node: dict):
    # emissions are set to 0 when not required to run, but we should still run for every model
    return node is not None and all([
        node.get('@type', node.get('type')) == 'Emission',
        'value' in node.get('added', [])
    ]) and node.get('value', [])[0] == 0


def should_run(data: dict, model: dict):
    key = get_required_model_param(model, 'key')
    term_id = get_required_model_param(model, 'value')
    args = model.get('runArgs', {})
    node = find_term_match(data.get(key, []), args.get('termId', term_id), None)

    # run if: value is empty or force run from args
    is_empty = _is_empty(node, args.get('skipEmptyValue', False))
    is_0_emission = _is_0_emission(node)
    run_is_aggregated = _run_aggregated(data, args.get('skipAggregated', False))
    run_args = {
        key: func(node) for key, func in _RUN_FROM_ARGS.items() if node and args.get(key, False) is True
    }
    run = any([
        is_empty,
        is_0_emission,
        (len(run_args.keys()) > 0 and all([v for _k, v in run_args.items()]))
    ]) and _run_required(data, model.get('model'), term_id) and run_is_aggregated

    logShouldRun(data, model.get('model'), term_id, run, key=key, value=term_id,
                 is_empty=is_empty,
                 is_0_emission=is_0_emission,
                 run_is_aggregated=run_is_aggregated,
                 **run_args)

    return run
