from functools import reduce
from hestia_earth.utils.tools import non_empty_list, flatten, list_sum
from hestia_earth.utils.blank_node import get_node_value

from hestia_earth.aggregation.log import logger
from hestia_earth.aggregation.utils import weighted_average, _min, _max, _sd
from hestia_earth.aggregation.utils.completeness import blank_node_completeness_key


def _debugNodes(nodes: list):
    for node in nodes:
        if node.get('yield'):
            logger.debug(
                'id=%s, yield=%s, weight=%s, ratio=%s/%s, organic=%s, irrigated=%s',
                node.get('@id'),
                round(node.get('yield')),
                100/len(nodes),
                1,
                len(nodes),
                node.get('organic'),
                node.get('irrigated')
            )


def _weighted_value(node: dict, key: str = 'value'):
    value = get_node_value(node, key)
    weight = node.get('productValue', 1)
    return None if (value is None or weight is None) else (value, weight)


def _completeness_count_missing(nodes: list, completeness: dict):
    first_node = nodes[0]
    completeness_key = blank_node_completeness_key(first_node)
    completeness_count = len([node for node in nodes if node.get('completeness', False)])
    completeness_count_total = completeness.get(completeness_key, 0)
    completeness_count_missing = (
        completeness_count_total - completeness_count
    ) if completeness_count_total > completeness_count else 0
    return completeness_count_missing


def _product_count_missing(complete_nodes: list):
    # add `0` values for complete products but wih no `value` (missing term or missing value)
    return len(list(filter(lambda node: len(node.get('value', [])) == 0, complete_nodes)))


def _aggregate(blank_nodes: list, completeness: dict, combine_values: bool):
    first_node = blank_nodes[0]
    term = first_node.get('term')
    is_product_aggregation = first_node['@type'] == 'Product'

    # only use nodes were completeness is True
    complete_nodes = [node for node in blank_nodes if node.get('completeness', False)]

    # for primary product, we can use the value only for incomplete products
    incomplete_products_with_value = [
        node for node in blank_nodes
        if all([not node.get('completeness', False), list_sum(node.get('value', [-1]), -1) > 0])
    ] if is_product_aggregation and first_node.get('primary') else []
    incomplete_values = non_empty_list(map(_weighted_value, incomplete_products_with_value))

    missing_weights = [(0, 1)] * (
        (_product_count_missing(complete_nodes) if is_product_aggregation else 0) +
        _completeness_count_missing(blank_nodes, completeness)
    )

    economicValueShare_values = non_empty_list([_weighted_value(node, 'economicValueShare') for node in complete_nodes])
    economicValueShare = weighted_average(economicValueShare_values + missing_weights)

    weighted_values = non_empty_list(map(_weighted_value, complete_nodes))
    values_with_missing_weight = weighted_values + missing_weights + incomplete_values

    values = [v for v, _w in values_with_missing_weight]

    if not values:
        logger.warning(f"No aggregated values found for '{term.get('@id')}'")

    # fallback to compile from values
    all_nodes = complete_nodes + incomplete_products_with_value
    all_values = [n.get('value', []) for n in all_nodes]

    max_value = _max(values) if not combine_values else _max(flatten([
        n.get('max', []) for n in all_nodes
    ] + all_values), min_observations=len(all_values) or 1)
    min_value = _min(values) if not combine_values else _min(flatten([
        n.get('min', []) for n in all_nodes
    ] + all_values), min_observations=len(all_values) or 1)
    observations = len(values) if not combine_values else sum(flatten([
        n.get('observations', 1) for n in all_nodes
    ])) + len(missing_weights)

    value = weighted_average(values_with_missing_weight)

    return {
        'nodes': complete_nodes,
        'node': first_node,
        'term': term,
        'economicValueShare': economicValueShare,
        'value': value,
        'max': max_value,
        'min': min_value,
        'sd': _sd(values),
        'observations': observations
    } if len(values) > 0 else None


def _aggregate_term(aggregates_map: dict, completeness: dict, combine_values: bool):
    def aggregate(term_id: str):
        blank_nodes = [node for node in aggregates_map.get(term_id, []) if not node.get('deleted')]
        return _aggregate(blank_nodes, completeness, combine_values) if len(blank_nodes) > 0 else None
    return aggregate


def _aggregate_nodes(aggregate_key: str, combine_values: bool, index=0):
    def aggregate(data: dict):
        if index == 0:
            _debugNodes(data.get('nodes', []))
        completeness = data.get('completeness', {})
        terms = data.get(aggregate_key).keys()
        aggregates = non_empty_list(map(
            _aggregate_term(data.get(aggregate_key), completeness, combine_values),
            terms
        ))
        return (aggregates, data) if len(aggregates) > 0 else ([], {})

    def aggregate_multiple(data: dict):
        return reduce(
            lambda prev, curr: {**prev, curr[1]: _aggregate_nodes(curr[1], curr[0])(data)}, enumerate(aggregate_key), {}
        )

    return aggregate if isinstance(aggregate_key, str) else aggregate_multiple


def aggregate(aggregate_key: str, groups: dict, combine_values: bool = False) -> list:
    return non_empty_list(map(_aggregate_nodes(aggregate_key, combine_values), groups.values()))
