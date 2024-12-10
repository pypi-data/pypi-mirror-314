import os
from decimal import Decimal
from statistics import stdev, mean
from functools import reduce
from hestia_earth.utils.tools import safe_parse_date

from ..version import VERSION
from .completeness import is_complete, group_completeness, update_completeness
from .term import _group_by_term_id
from .practice import filter_practices
from .blank_node import filter_blank_nodes

MIN_NB_OBSERVATIONS = 20


def create_folders(filepath: str): return os.makedirs(os.path.dirname(filepath), exist_ok=True)


def _save_json(data: dict, filename: str):
    import os
    should_run = os.getenv('DEBUG', 'false') == 'true'
    if not should_run:
        return
    import json
    dir = os.getenv('TMP_DIR', '/tmp')
    filepath = f"{dir}/{filename}.jsonld"
    create_folders(filepath)
    with open(filepath, 'w') as f:
        return json.dump(data, f, indent=2)


def sum_data(nodes: list, key: str): return sum([node.get(key, 1) for node in nodes])


def _aggregated_node(node: dict):
    return {**node, 'aggregated': True, 'aggregatedVersion': VERSION}


def _aggregated_version(node: dict, *keys):
    node['aggregated'] = node.get('aggregated', [])
    node['aggregatedVersion'] = node.get('aggregatedVersion', [])
    all_keys = ['value'] if len(keys) == 0 else keys
    for key in all_keys:
        if node.get(key) is None:
            continue
        if key in node['aggregated']:
            node.get('aggregatedVersion')[node['aggregated'].index(key)] = VERSION
        else:
            node['aggregated'].append(key)
            node['aggregatedVersion'].append(VERSION)
    return node


def _min(values, observations: int = 0, min_observations: int = MIN_NB_OBSERVATIONS):
    return min(values) if (observations or len(values)) >= min_observations else None


def _max(values, observations: int = 0, min_observations: int = MIN_NB_OBSERVATIONS):
    return max(values) if (observations or len(values)) >= min_observations else None


def _sd(values): return stdev(values) if len(values) >= 2 else None


def _numeric_weighted_average(values: list):
    total_weight = sum(Decimal(str(weight)) for _v, weight in values) if values else Decimal(0)
    weighted_values = [Decimal(str(value)) * Decimal(str(weight)) for value, weight in values]
    average = sum(weighted_values) / (total_weight if total_weight else 1) if weighted_values else None
    return None if average is None else float(average)


def _bool_weighted_average(values: list):
    return mean(map(int, values)) >= 0.5


def weighted_average(weighted_values: list):
    values = [v for v, _w in weighted_values]
    all_boolean = all([isinstance(v, bool) for v in values])
    return None if not values else (
        _bool_weighted_average(values) if all_boolean else _numeric_weighted_average(weighted_values)
    )


def _unique_nodes(nodes: list): return list({n.get('@id'): n for n in nodes}.values())


def sum_values(values: list):
    """
    Sum up the values while handling `None` values.
    If all values are `None`, the result is `None`.
    """
    filtered_values = [v for v in values if v is not None]
    return sum(filtered_values) if len(filtered_values) > 0 else None


def _set_dict_single(data: dict, key: str, value, strict=False):
    if value is not None and (not strict or value != 0):
        data[key] = value
    return data


def _set_dict_array(data: dict, key: str, value, strict=False):
    if data is not None and value is not None and (not strict or value != 0):
        data[key] = [value]
    return data


def _end_date_year(node: dict):
    date = safe_parse_date(node.get('endDate'))
    return date.year if date else None


def _same_product(product: dict):
    def compare(node: dict):
        np = node.get('product', {}) if node else {}
        return np.get('@id', np.get('term', {}).get('@id')) == product.get('@id')
    return compare


GROUP_BY_METHOD_MODEL_PROP = [
    'emissionsResouceUse',
    'impacts',
    'endpoints'
]


_FILTER_BLANK_NODES = {
    'practices': filter_practices,
    'measurements': filter_blank_nodes
}


def _filter_blank_nodes(node: dict, list_key: str, start_year: int, end_year: int):
    blank_nodes = node.get(list_key, [])
    return _FILTER_BLANK_NODES.get(list_key, lambda values, *args: values)(blank_nodes, start_year, end_year)


def group_by_product(product: dict, nodes: list, props: list, start_year: int, end_year: int, include_matrix=True):
    """
    Group a list of blank nodes filtering by the same product.
    """
    filtered_nodes = list(filter(_same_product(product), map(update_completeness, nodes)))

    def group_by(group: dict, node: dict):
        node_id = node.get('@id', node.get('id'))
        end_date = _end_date_year(node)
        organic = node.get('organic', False)
        irrigated = node.get('irrigated', False)
        key = '-'.join([str(organic), str(irrigated)]) if include_matrix else ''
        data = {
            'organic': organic,
            'irrigated': irrigated,
            'country': node.get('country'),
            'year': end_date
        }
        if key not in group:
            group[key] = {
                'product': product,
                'nodes': [],
                'sites': [],
                'completeness': {},
                **data,
                **reduce(lambda prev, curr: {**prev, curr: {}}, props, {})
            }
        group[key]['nodes'].append({**node, **data})
        group[key]['sites'].append(node.get('site'))

        def group_by_prop(list_key: str):
            blank_nodes = _filter_blank_nodes(node, list_key, start_year, end_year)
            # save ref to organic/irrigated for later grouping
            values = list(map(
                lambda v: {
                    **v,
                    **data,
                    'id': node_id,
                    'completeness': is_complete(node, product, v)
                }, blank_nodes))
            return reduce(_group_by_term_id(list_key in GROUP_BY_METHOD_MODEL_PROP), values, group[key][list_key])

        group[key] = reduce(lambda prev, curr: {**prev, curr: group_by_prop(curr)}, props, group[key])
        group[key]['completeness'] = group_completeness(group[key]['completeness'], node, product)
        return group

    return reduce(group_by, filtered_nodes, {})


def value_difference(value: float, expected_value: float):
    """
    Get the difference in percentage between a value and the expected value.

    Parameters
    ----------
    value : float
        The value to check.
    expected_value : float
        The expected value.

    Returns
    -------
    bool
        The difference in percentage between the value and the expected value.
    """
    return 0 if (isinstance(expected_value, list) and len(expected_value) == 0) or expected_value == 0 else (
        round(abs(value - expected_value) / expected_value, 4)
    )
