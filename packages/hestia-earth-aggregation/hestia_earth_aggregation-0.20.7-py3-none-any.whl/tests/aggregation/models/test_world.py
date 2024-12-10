from unittest.mock import patch
import json

from tests.utils import (
    overwrite_expected,
    PRODUCT_BY_FILENAME, SOURCE, WORLD, fixtures_path, start_year, end_year,
    fake_download, fake_aggregated_version, filter_cycles
)
from hestia_earth.aggregation.utils import group_by_product
from hestia_earth.aggregation.models.world import aggregate
from hestia_earth.aggregation.cycle.utils import (
    AGGREGATION_KEYS, format_for_grouping, _update_cycle, _format_world_results
)
from hestia_earth.aggregation.utils.quality_score import calculate_score

class_path = 'hestia_earth.aggregation.models.world'


@patch('hestia_earth.aggregation.cycle.emission._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.input._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.practice.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.cycle.practice._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.product._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.utils._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.utils._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.utils._timestamp', return_value='')
@patch('hestia_earth.aggregation.utils.measurement._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.queries.download_hestia', side_effect=fake_download)
def test_aggregate_cycle_wheatGrain(*args):
    expected_path = f"{fixtures_path}/cycle/world/wheatGrain-aggregated.jsonld"
    with open(f"{fixtures_path}/cycle/countries/wheatGrain-aggregated.jsonld", encoding='utf-8') as f:
        cycles = json.load(f)
    with open(expected_path, encoding='utf-8') as f:
        expected = json.load(f)

    cycles = format_for_grouping(filter_cycles(cycles))
    product = PRODUCT_BY_FILENAME['wheatGrain']
    results = aggregate(AGGREGATION_KEYS, group_by_product(product, cycles, AGGREGATION_KEYS, 1950, 2050, False))
    results = list(map(_format_world_results, results))
    results = list(map(_update_cycle(WORLD, start_year, end_year, SOURCE, False), results))
    results = list(map(calculate_score, results))
    results = results
    overwrite_expected(expected_path, results)
    assert results == expected


@patch('hestia_earth.aggregation.cycle.emission._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.input._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.practice.download_hestia', side_effect=fake_download)
@patch('hestia_earth.aggregation.cycle.practice._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.product._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.utils._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.utils._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.cycle.utils._timestamp', return_value='')
@patch('hestia_earth.aggregation.utils.measurement._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_version', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.site._aggregated_node', side_effect=fake_aggregated_version)
@patch('hestia_earth.aggregation.utils.queries.download_hestia', side_effect=fake_download)
def test_aggregate_cycle_bananaFruit(*args):
    expected_path = f"{fixtures_path}/cycle/world/bananaFruit-aggregated.jsonld"
    with open(f"{fixtures_path}/cycle/countries/bananaFruit-aggregated.jsonld", encoding='utf-8') as f:
        cycles = json.load(f)
    with open(expected_path, encoding='utf-8') as f:
        expected = json.load(f)

    cycles = format_for_grouping(filter_cycles(cycles))
    product = PRODUCT_BY_FILENAME['bananaFruit']
    results = aggregate(AGGREGATION_KEYS, group_by_product(product, cycles, AGGREGATION_KEYS, 1950, 2050, False))
    results = list(map(_format_world_results, results))
    results = list(map(_update_cycle(WORLD, start_year, end_year, SOURCE, False), results))
    results = list(map(calculate_score, results))
    results = results
    overwrite_expected(expected_path, results)
    assert results == expected
