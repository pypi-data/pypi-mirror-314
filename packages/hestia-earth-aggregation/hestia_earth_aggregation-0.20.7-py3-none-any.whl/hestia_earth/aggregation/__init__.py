from pkgutil import extend_path
from hestia_earth.utils.tools import current_time_ms

from .log import logger
from .utils.queries import find_nodes
from .utils.source import get_source
from .utils.term import _is_global
from .cycle import aggregate_global, aggregate_country

__path__ = extend_path(__path__, __name__)


def aggregate(country: dict, product: dict, start_year: int, end_year: int, source: dict):
    """
    Aggregates data from HESTIA.
    Produced data will be aggregated by product, country and year.

    Parameters
    ----------
    country: dict
        The country to group the data.
    product: dict
        The product to group the data.
    start_year: int
        The start year of the data.
    end_year: int
        The end year of the data.
    source: dict
        Optional - the source of the generate data. Will be set to HESTIA if not provided.

    Returns
    -------
    list
        A list of aggregations.
        Example: `[<impact_assesment1>, <impact_assesment2>, <cycle1>, <cycle2>]`
    """
    now = current_time_ms()

    nodes = find_nodes(product, start_year, end_year, country)
    is_global = _is_global(country)
    aggregate_func = aggregate_global if is_global else aggregate_country
    aggregations = aggregate_func(
        country, product, nodes, source or get_source(), start_year, end_year
    ) if len(nodes) > 0 else []

    logger.info('time=%s, unit=ms', current_time_ms() - now)

    return aggregations
