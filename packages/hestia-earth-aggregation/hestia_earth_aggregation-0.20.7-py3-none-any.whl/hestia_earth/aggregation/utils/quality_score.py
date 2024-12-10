import os
from enum import Enum
from functools import reduce
from hestia_earth.schema import SchemaType, TermTermType, AGGREGATED_QUALITY_SCORE_FIELDS
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.tools import list_sum, safe_parse_float
from hestia_earth.utils.emission import cycle_emission_is_in_system_boundary, cycle_emissions_in_system_boundary

from hestia_earth.aggregation.log import debugRequirements
from . import value_difference
from .lookup import production_quantity_lookup, production_quantity_country

FAOSTAT_PRODUCTION_LOOKUP_COLUMN = 'cropGroupingFaostatProduction'
YIELD_THRESHOLD = 20
REGION_PRODUCTION_THRESHOLD = 75
COMPLETENESS_SCORE_FIELDS = AGGREGATED_QUALITY_SCORE_FIELDS.get(SchemaType.COMPLETENESS.value, [])
KEY = 'aggregatedQualityScore'
KEY_MAX = KEY + 'Max'


class ScoreKeys(Enum):
    YIELD = 'yield'
    NB_CYCLES = 'nb_cycles'
    COMPLETENESS = 'completeness'
    EMISSIONS_SYSTEM_BOUNDARY = 'emissions_system_boundary'
    REGION_PRODUCTION_RATIO = 'countries_production_ratio'


def _faostat_crop_grouping(term_id: str):
    lookup = download_lookup('crop.csv')
    return get_table_value(lookup, 'termid', term_id, column_name(FAOSTAT_PRODUCTION_LOOKUP_COLUMN))


def _faostat_crop_yield(country_id: str, grouping: str, date: int):
    lookup = download_lookup(f"region-crop-{FAOSTAT_PRODUCTION_LOOKUP_COLUMN}-yield.csv")
    value = get_table_value(lookup, 'termid', country_id, column_name(grouping))
    value = safe_parse_float(extract_grouped_data_closest_date(value, date), None)
    # value in lookup is in kg/ha
    return round(value, 4) if value is not None else None


def _calculate_score_yield(cycle: dict, *args):
    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    year = int(cycle.get('endDate'))
    product = find_primary_product(cycle)
    grouping = _faostat_crop_grouping((product or {}).get('term', {}).get('@id'))
    faostat_yield = _faostat_crop_yield(country_id, grouping, year) if grouping else None
    product_yield = list_sum(product.get('value')) if product else None
    delta = value_difference(product_yield, faostat_yield) * 100 if all([faostat_yield, product_yield]) else None

    debugRequirements(id=cycle.get('id'),
                      country_id=country_id,
                      cycle_year=year,
                      faostat_grouping=grouping,
                      faostat_yield=faostat_yield,
                      product_yield=product_yield,
                      yield_delta=delta,
                      yield_delta_min=YIELD_THRESHOLD,
                      yield_delta_threshold=YIELD_THRESHOLD)

    return delta <= YIELD_THRESHOLD if delta is not None else False


def _production_delta(cycle: dict, countries: list, lookup, lookup_column: str):
    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    year = int(cycle.get('endDate'))
    global_value = production_quantity_country(lookup, lookup_column, year, country_id=country_id)
    country_values = [
        production_quantity_country(lookup, lookup_column, year, country_id=country.get('@id')) for country in countries
    ]
    total_value = list_sum(country_values)
    delta = (total_value / global_value) * 100 if global_value and total_value else None

    debugRequirements(id=cycle.get('id'),
                      country_id=country_id,
                      cycle_year=year,
                      region_production_quantity=global_value,
                      countries_production_quantity=total_value,
                      production_delta=delta,
                      production_delta_min=REGION_PRODUCTION_THRESHOLD)

    return delta


def _calculate_score_region_production(cycle: dict, countries: list):
    product = find_primary_product(cycle)
    term = (product or {}).get('term', {})
    lookup, lookup_column = production_quantity_lookup(term)
    delta = _production_delta(cycle, countries, lookup, lookup_column) if lookup is not None else None
    return delta >= REGION_PRODUCTION_THRESHOLD if delta is not None else False


def _calculate_score_nb_cycles(cycle: dict, *args):
    nb_observations = cycle.get('numberOfCycles', 1)

    debugRequirements(id=cycle.get('id'),
                      nb_observations=nb_observations)

    return nb_observations >= 50


def _calculate_score_completeness(cycle: dict, *args):
    completeness: dict = cycle.get('completeness', {})
    completeness_keys = [k for k in completeness.keys() if k in COMPLETENESS_SCORE_FIELDS]
    is_complete = all([bool(completeness.get(k)) for k in completeness_keys])
    incomplete_keys = [k for k in completeness_keys if not bool(completeness.get(k))]

    debugRequirements(id=cycle.get('id'),
                      is_complete=is_complete,
                      completeness_keys=';'.join(completeness_keys),
                      incomplete_keys=';'.join(incomplete_keys))

    return is_complete


def _calculate_score_emissions_system_boundary(cycle: dict, *args):
    all_emissions_ids = cycle_emissions_in_system_boundary(cycle)

    emissions_ids = list(set([e.get('term', {}).get('@id') for e in cycle.get('emissions', [])]))
    emissions_ids = list(filter(cycle_emission_is_in_system_boundary(cycle), emissions_ids))

    missing_emissions = list(filter(lambda term_id: term_id not in emissions_ids, all_emissions_ids))
    all_included = len(missing_emissions) == 0

    debugRequirements(id=cycle.get('id'),
                      total_emissions_in_system_boundary=len(all_emissions_ids),
                      included_emissions=len(emissions_ids),
                      all_included=all_included,
                      missing_emissions=';'.join(missing_emissions))

    return all_included


_FUNC_SCORE_KEY = {
    ScoreKeys.YIELD: _calculate_score_yield,
    ScoreKeys.COMPLETENESS: _calculate_score_completeness,
    ScoreKeys.EMISSIONS_SYSTEM_BOUNDARY: _calculate_score_emissions_system_boundary,
    ScoreKeys.NB_CYCLES: _calculate_score_nb_cycles,
    ScoreKeys.REGION_PRODUCTION_RATIO: _calculate_score_region_production,
}


def _should_run_crop(cycle: dict, *args):
    product = find_primary_product(cycle)
    term = (product or {}).get('term', {})
    return term.get('termType') == TermTermType.CROP.value


_RUN_SCORE_KEY = {
    ScoreKeys.YIELD: _should_run_crop,
    ScoreKeys.REGION_PRODUCTION_RATIO: lambda cycle, countries: len(countries) > 0 and _should_run_crop(cycle)
}


def calculate_score(cycle: dict, countries: list = []):
    score_keys = [e for e in ScoreKeys if _RUN_SCORE_KEY.get(e, lambda *args: True)(cycle, countries)]
    score = reduce(
        lambda total, key: total + (1 if _FUNC_SCORE_KEY.get(key)(cycle, countries) else 0), score_keys, 0
    )
    return {
        **cycle,
        KEY: score,
        KEY_MAX: len(score_keys)
    }


def _enable_filter_min_score(): return os.getenv('AGGREGATION_MAX_SCORE_ENABLED', 'true') == 'true'


def _min_score_diff(): return int(os.getenv('AGGREGATION_MAX_SCORE_DIFF', '2'))


def _has_min_score(data: dict):
    # aggregation is only valid if score is more than max-2 by default
    return all([
        # if ImpactAssessment is created without a Cycle, this will ignore the IA.
        data.get(KEY, 0) >= 0,
        data.get(KEY_MAX, 0) - data.get(KEY, 0) <= _min_score_diff()
    ])


def filter_min_score(values: list):
    return list(filter(_has_min_score, values)) if _enable_filter_min_score() else list(values)
