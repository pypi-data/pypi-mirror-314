import requests
import json
import math
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from hestia_earth.schema import NodeType, TermTermType, PRODUCT_TERM
from hestia_earth.utils.api import download_hestia, find_node, _safe_post_request
from hestia_earth.utils.tools import non_empty_list
from hestia_earth.utils.request import api_url
from hestia_earth.utils.storage._s3_client import _get_s3_client, _get_bucket

from hestia_earth.aggregation.log import logger
from . import _save_json
from .term import DEFAULT_COUNTRY_NAME, should_aggregate, _format_country_name, _fetch_countries, _is_global

# TODO paginate results
SEARCH_LIMIT = 10000
MATCH_AGGREGATED_QUERY = {'match': {'aggregated': 'true'}}
# aggregate every 20 years
TIME_PERIOD = 20


def _date_range_query(start: int, end: int):
    return {'range': {'endDate': {'gte': str(start), 'lte': str(end)}}} if start and end else None


def _product_query(product_name: str = None, match_aggregated=False):
    return {
        'bool': {
            'must': non_empty_list([
                {'match': {'@type': NodeType.CYCLE.value}},
                {
                    'nested': {
                        'path': 'products',
                        'query': {
                            'bool': {
                                'must': [
                                    {'match': {'products.term.name.keyword': product_name}},
                                    {'match': {'products.primary': 'true'}}
                                ]
                            }
                        }
                    }
                } if product_name else None,
                MATCH_AGGREGATED_QUERY if match_aggregated else None
            ]),
            'must_not': non_empty_list([
                None if match_aggregated else MATCH_AGGREGATED_QUERY
            ])
        }
    }


COUNTRY_FIELD_BY_TYPE = {
    NodeType.CYCLE.value: 'site.country'
}


def _country_query(country_name: str):
    return {'match': {'site.country.name.keyword': country_name}}


def _run_query(data: dict):
    headers = {'Content-Type': 'application/json'}
    params = json.dumps(data)
    return requests.post(f'{api_url()}/search', params, headers=headers).json().get('results', [])


def _download_by_state(node: dict, data_state: str):
    try:
        node = download_hestia(node.get('@id'), node.get('@type'), data_state=data_state)
        return node if node.get('@type') else None
    except Exception:
        logger.debug('skip non-%s %s: %s', data_state, node.get('@type'), node.get('@id'))
        return None


def _download_recalculated_node(node: dict, data_state: str):
    key = '/'.join([data_state, node.get('@type'), f"{node.get('@id')}.jsonld"])

    # try to download from S3 and make sure last stage is reached, otherwise skip
    try:
        content = _get_s3_client().get_object(Bucket=_get_bucket(), Key=key)
        metadata = content.get('Metadata', {})
        is_max_stage = metadata.get('stage', 1) == metadata.get('maxstage', 1)
        body = content.get('Body')
        return json.loads(body.read()) if is_max_stage and body else None
    except ImportError:
        return _download_by_state(node, data_state)


def download_node(node: dict):
    data_state = (
        # no stage for aggregated node as only IA is recalculated
        'recalculated' if node.get('@type') in [NodeType.IMPACTASSESSMENT.value] else 'original'
    ) if node.get('aggregated', False) else 'recalculated'
    download_function = _download_recalculated_node if data_state == 'recalculated' else _download_by_state
    return download_function(node, data_state)


def _download_nodes(nodes: list):
    total = len(nodes)
    with ThreadPoolExecutor() as executor:
        nodes = non_empty_list(executor.map(download_node, nodes))
    logger.debug('downloaded %s nodes / %s total nodes', str(len(nodes)), str(total))
    return nodes


def _country_nodes_query(product_name: str, start_year: int, end_year: int, country_name: str):
    query = _product_query(product_name)
    date_range = _date_range_query(start_year, end_year)
    query['bool']['must'].extend([date_range] if date_range else [])
    if country_name != DEFAULT_COUNTRY_NAME:
        query['bool']['must'].append(_country_query(country_name))

    return {
        'query': query,
        'limit': SEARCH_LIMIT,
        'fields': ['@id', '@type']
    }


def _country_nodes(product_name: str, start_year: int, end_year: int, country_name: str):
    # TODO: paginate search and improve performance
    nodes = _run_query(_country_nodes_query(product_name, start_year, end_year, country_name))
    return _download_nodes(nodes)


def _global_query(product_name: str, start_year: int, end_year: int):
    countries = _fetch_countries()
    query = {
        'bool': {
            'must': non_empty_list([
                _product_query(product_name, match_aggregated=True),
                MATCH_AGGREGATED_QUERY,
                _date_range_query(start_year, end_year)
            ]),
            'must_not': [
                # do not include lower levels of country breakdown
                {'match': {'name': 'Conventional'}},
                {'match': {'name': 'Irrigated'}},
                {'match': {'name': 'Organic'}}
            ],
            'should': [
                _country_query(country.get('name')) for country in countries
            ],
            'minimum_should_match': 1
        }
    }
    return {
        'query': query,
        'limit': SEARCH_LIMIT,
        'fields': ['@id', '@type', 'aggregated']
    }


def _global_nodes(product_name: str, start_year: int, end_year: int):
    nodes = _run_query(_global_query(product_name, start_year, end_year))
    return _download_nodes(nodes)


def _sub_country_nodes(product: dict, start_year: int, end_year: int, region_name: str):
    sub_regions = _run_query({
        'query': {
            'bool': {
                'must': [
                    {'match': {'@type': NodeType.TERM.value}},
                    {'match': {'termType': TermTermType.REGION.value}},
                    {'match': {'subClassOf.name.keyword': region_name}}
                ]
            }
        },
        'limit': SEARCH_LIMIT,
        'fields': ['@id', 'name']
    })
    nodes = [{
        '@type': NodeType.CYCLE.value,
        '@id': '-'.join([
            product.get('@id'),
            _format_country_name(v['name']),
            str(start_year),
            str(end_year)
        ]),
        'aggregated': True
    } for v in sub_regions]
    return _download_nodes(nodes)


def find_nodes(product: dict, start_year: int, end_year: int, country: dict):
    product_name = product.get('name')
    country_name = country.get('name')
    nodes = (
        _sub_country_nodes(
            product, start_year, end_year, country_name
        ) if _is_global(country) else _country_nodes(
            product_name, start_year, end_year, country_name
        )
    ) if country_name != DEFAULT_COUNTRY_NAME else _global_nodes(
        product_name, start_year, end_year
    )
    _save_json({'nodes': nodes}, '-'.join([
        str(v) for v in ['nodes', product_name, country_name, start_year, end_year] if v
    ]))
    return nodes


def count_nodes(product: dict, start_year: int, end_year: int, country: dict):
    """
    Return the number of Nodes that will be used to aggregate.
    """
    product_name = product.get('name')
    country_name = country.get('name')
    query = (
        -1 if _is_global(country) else _country_nodes_query(product_name, start_year, end_year, country_name)
    ) if country_name != DEFAULT_COUNTRY_NAME else _global_query(product_name, start_year, end_year)
    return _safe_post_request(f"{api_url()}/count", query)


def get_countries():
    """
    Get the list of countries (GADM level 0 regions).

    Returns
    -------
    list
        The list of countries as `dict`.
    """
    return find_node(NodeType.TERM, {'termType': TermTermType.REGION.value, 'gadmLevel': 0}, limit=1000)


def get_continents():
    """
    Get the list of continents (GADM level 0 regions prefixed by `region-` with a `subClassOf` != `region-world`).

    Returns
    -------
    list
        The list of countries as `dict`.
    """
    query = {
        'bool': {
            'must': [
                {'match': {'@type': NodeType.TERM.value}},
                {'match': {'termType': TermTermType.REGION.value}},
                {'regexp': {'@id': 'region-*'}},
                {'match': {'subClassOf.subClassOf.name.keyword': DEFAULT_COUNTRY_NAME}}
            ],
            'must_not': [
                {'match': {'subClassOf.name.keyword': DEFAULT_COUNTRY_NAME}}
            ]
        }
    }
    params = {
        'query': query,
        'limit': 1000,
        'fields': ['@type', '@id', 'name']
    }
    return _run_query(params)


def get_products():
    """
    Get the list of terms that can be used to aggregate.

    Returns
    -------
    list
        The list of terms as `dict`.
    """
    query = {
        'bool': {
            'must': [{'match': {'@type': NodeType.TERM.value}}],
            'should': [
                {'match': {'termType.keyword': type.value}} for type in PRODUCT_TERM
            ],
            'minimum_should_match': 1
        }
    }
    params = {
        'query': query,
        'limit': 10000,
        'fields': ['@type', '@id', 'name', 'termType'],
        'sort': [{'termType.keyword': 'asc'}]
    }
    terms = _run_query(params)
    return list(filter(should_aggregate, terms))


def _get_time_ranges(earliest_date: str, latest_date: str, period_length: int = TIME_PERIOD):
    """
    Get time ranges starting from the earliest date to today.

    Parameters
    ----------
    earliest_date : str
        The start date of the time range.
    latest_date : str
        The end date of the time range.
    period_length : int
        Optional - length of the period, 20 by default.

    Returns
    -------
    list
        A list of time periods.
        Example: `[(1990, 2009), (2010, 2024)]`
    """
    earliest_year = int(earliest_date[0:4])
    latest_year = int(latest_date[0:4])

    # start from the minimum century - 10 years. Go every X years. Filter for dates that contain min/max
    min_year = round(math.floor(earliest_year / 100) * 100) - 10
    max_year = datetime.now().year
    periods = [(i, min(i+period_length-1, datetime.now().year)) for i in range(min_year, max_year, period_length)]
    logger.debug('Time ranges between %s and %s: %s', min_year, max_year, periods)
    return [(start, end) for (start, end) in periods if any([
        start <= earliest_year <= end,
        earliest_year <= start and end <= latest_year,
        start <= latest_year <= end
    ])]


def _earliest_date(product_name: str, country: dict):
    is_global = _is_global(country)
    query = _product_query(product_name, match_aggregated=is_global)
    if not is_global:
        query['bool']['must'].append(_country_query(country.get('name')))
    params = {
        'query': query,
        'limit': 1,
        'fields': ['endDate'],
        'sort': [{'endDate.keyword': 'asc'}]
    }
    results = _run_query(params)
    return results[0].get('endDate') if len(results) > 0 else None


def _latest_date(product_name: str, country: dict):
    is_global = _is_global(country)
    query = _product_query(product_name, match_aggregated=is_global)
    if not is_global:
        query['bool']['must'].append(_country_query(country.get('name')))
    params = {
        'query': query,
        'limit': 1,
        'fields': ['endDate'],
        'sort': [{'endDate.keyword': 'desc'}]
    }
    results = _run_query(params)
    return results[0].get('endDate') if len(results) > 0 else None


def get_time_ranges(country: dict, product_name: str):
    from_date = _earliest_date(product_name, country)
    to_date = _latest_date(product_name, country) if from_date else None
    return _get_time_ranges(from_date, to_date) if to_date else []
