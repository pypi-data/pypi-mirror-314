from functools import reduce
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.tools import non_empty_list, safe_parse_float, flatten, list_sum
from hestia_earth.utils.blank_node import get_node_value

from hestia_earth.aggregation.log import debugWeights, debugRequirements
from hestia_earth.aggregation.utils import weighted_average, _end_date_year, _min, _max, _sd
from hestia_earth.aggregation.utils.term import (
    DEFAULT_COUNTRY_ID, _format_organic, _format_irrigated
)
from hestia_earth.aggregation.utils.completeness import blank_node_completeness_key


def _organic_weight(country_id: str, year: int):
    lookup = download_lookup('region-standardsLabels-isOrganic.csv')
    data = get_table_value(lookup, 'termid', country_id, 'organic')
    # default to 0 => assume nothing organic
    value = safe_parse_float(extract_grouped_data_closest_date(data, year), None)

    debugRequirements(country_id=country_id, year=year,
                      organic_weight=value)

    return min(1, value / 100) if value else None


def _irrigated_weight(country_id: str, year: int, siteType: str = 'all'):
    lookup = download_lookup('region-irrigated.csv')

    total_area_data = get_table_value(lookup, 'termid', country_id, column_name(siteType))
    # default to 1 => assume whole area
    total_area = safe_parse_float(extract_grouped_data_closest_date(total_area_data, year), 1)

    irrigated_data = get_table_value(lookup, 'termid', country_id, column_name(f"{siteType} irrigated"))
    irrigated = safe_parse_float(extract_grouped_data_closest_date(irrigated_data, year), None)

    debugRequirements(country_id=country_id, year=year,
                      site_type=siteType,
                      total_area=total_area,
                      irrigated_area=irrigated)

    return irrigated / total_area if irrigated else None


def _add_weights(country_id: str, year: int):
    def apply(prev: dict, node: dict):
        organic_weight = _organic_weight(country_id, year) or _organic_weight(DEFAULT_COUNTRY_ID, year)
        irrigated_weight = (
            _irrigated_weight(country_id, year, 'cropland') or
            _irrigated_weight(country_id, year, 'agriculture') or
            _irrigated_weight(country_id, year) or
            0
        )
        weight = (
            organic_weight if node.get('organic', False) else 1-organic_weight
        ) * (
            irrigated_weight if node.get('irrigated', False) else 1-irrigated_weight
        )
        return {**prev, node.get('id'): {'weight': weight, 'completeness': node.get('completeness', {})}}
    return apply


def _weighted_value(weights: dict, key: str = 'value'):
    def apply(node: dict):
        value = get_node_value(node, key)
        weight = weights.get(node.get('id'), {}).get('weight')
        return None if (value is None or weight is None) else (value, weight)
    return apply


def _missing_weights(nodes: list):
    completeness_key = blank_node_completeness_key(nodes[0])
    keys = ['-'.join([
        _format_organic(node.get('organic')), _format_irrigated(node.get('irrigated'))
    ]) for node in nodes]

    def apply(item: tuple):
        key, weight = item
        is_complete = weight.get('completeness', {}).get(completeness_key, False)
        is_missing = all([k not in key for k in keys])
        return (0, weight.get('weight')) if is_complete and is_missing else None
    return apply


def _product_rescale_ratio(nodes: list, weights: dict):
    all_weights = list_sum(non_empty_list([w.get('weight') for w in weights.values()]))
    node_weights = list_sum([weights.get(node.get('id'), {}).get('weight') for node in nodes])
    return node_weights / all_weights


def _aggregate_weighted(nodes: list, weights: dict):
    first_node = nodes[0]
    term = first_node.get('term')

    # account for complete missing values
    missing_weights = non_empty_list(map(_missing_weights(nodes), weights.items()))

    rescale_ratio = _product_rescale_ratio(nodes, weights) if first_node['@type'] == 'Product' else 1

    economicValueShare = weighted_average(
        non_empty_list(map(_weighted_value(weights, 'economicValueShare'), nodes))
    )

    values_with_weight = non_empty_list(map(_weighted_value(weights), nodes)) + missing_weights
    value = weighted_average(values_with_weight)
    values = [value * rescale_ratio for value, _w in values_with_weight]

    observations = sum(flatten([n.get('observations', 1) for n in nodes])) + len(missing_weights)

    return {
        'nodes': nodes,
        'node': first_node,
        'term': term,
        'economicValueShare': economicValueShare * rescale_ratio if economicValueShare else None,
        'value': value * rescale_ratio if len(values) > 0 else None,
        'min': _min(values, observations),
        'max': _max(values, observations),
        'sd': _sd(values),
        'observations': observations
    }


def _aggregate_nodes(aggregate_key: str, weights: dict):
    def aggregate(data: dict):
        def aggregate(term_id: str):
            blank_nodes = data.get(aggregate_key).get(term_id)
            return _aggregate_weighted(blank_nodes, weights)

        aggregates = flatten(map(aggregate, data.get(aggregate_key, {}).keys()))
        return (aggregates, data) if len(aggregates) > 0 else ([], {})

    def aggregate_multiple(data: dict):
        return reduce(
            lambda prev, curr: {**prev, curr: _aggregate_nodes(curr, weights)(data)}, aggregate_key, {}
        )

    return aggregate if isinstance(aggregate_key, str) else aggregate_multiple


def aggregate(aggregate_key: str, groups: dict) -> list:
    nodes = next((data.get('nodes') for data in groups.values() if len(data.get('nodes', [])) > 0), [])
    first_node = nodes[0]
    country_id = first_node.get('country').get('@id')
    year = _end_date_year(first_node)
    weights = reduce(_add_weights(country_id, year), nodes, {})
    debugWeights(weights)
    return non_empty_list(map(_aggregate_nodes(aggregate_key, weights), groups.values()))
