from hestia_earth.utils.tools import non_empty_list

from hestia_earth.aggregation.log import logger
from hestia_earth.aggregation.utils import group_by_product
from hestia_earth.aggregation.models.terms import aggregate as aggregate_by_term
from hestia_earth.aggregation.models.countries import aggregate as aggregate_by_country
from hestia_earth.aggregation.models.world import aggregate as aggregate_world
from hestia_earth.aggregation.utils.quality_score import calculate_score, filter_min_score
from .utils import (
    AGGREGATION_KEYS,
    aggregate_with_matrix,
    format_for_grouping, _format_terms_results, _format_country_results, _format_world_results,
    _update_cycle
)


def aggregate_country(country: dict, product: dict, cycles: list, source: dict, start_year: int, end_year: int) -> list:
    include_matrix = aggregate_with_matrix(product)

    # step 1: aggregate all cycles indexed on the platform
    cycles = group_by_product(
        product, format_for_grouping(cycles), AGGREGATION_KEYS, start_year, end_year, include_matrix
    )
    # current product might not be any primary product in cycles
    if len(cycles.keys()) == 0:
        logger.debug('1 - No cycles to run aggregation.')
        return []

    aggregates = aggregate_by_term(AGGREGATION_KEYS, cycles)
    cycles = non_empty_list(map(_format_terms_results, aggregates))
    cycles = non_empty_list(map(_update_cycle(country, start_year, end_year, source, include_matrix), cycles))
    logger.debug(f"Found {len(cycles)} cycles at sub-country level")
    cycles = filter_min_score(map(calculate_score, cycles))
    if len(cycles) == 0:
        logger.debug('2 - No cycles to run aggregation.')
        return []

    # step 2: use aggregated cycles to calculate country-level cycles
    country_cycles = group_by_product(
        product, format_for_grouping(cycles), AGGREGATION_KEYS, start_year, end_year, False
    )
    aggregates = aggregate_by_country(AGGREGATION_KEYS, country_cycles)
    country_cycles = non_empty_list(map(_format_country_results, aggregates))
    country_cycles = non_empty_list(map(_update_cycle(country, start_year, end_year, source, False), country_cycles))
    logger.debug(f"Found {len(country_cycles)} cycles at country level")
    country_cycles = filter_min_score(map(calculate_score, country_cycles))

    # when not including matrix, cycles and country_cycles will be the same
    all_cycles = (cycles if include_matrix else []) + country_cycles
    return all_cycles


def aggregate_global(country: dict, product: dict, cycles: list, source: dict, start_year: int, end_year: int) -> list:
    cycles = format_for_grouping(cycles)
    countries = [cycle.get('site', {}).get('country') for cycle in cycles]
    cycles = group_by_product(product, cycles, AGGREGATION_KEYS, start_year, end_year, False)
    # current product might not be any primary product in cycles
    if len(cycles.keys()) == 0:
        return []

    aggregates = aggregate_world(AGGREGATION_KEYS, cycles)
    cycles = non_empty_list(map(_format_world_results, aggregates))
    cycles = non_empty_list(map(_update_cycle(country, start_year, end_year, source, False), cycles))
    cycles = filter_min_score([calculate_score(cycle, countries) for cycle in cycles])

    return cycles
