from unittest.mock import patch
import json

from tests.utils import (
    overwrite_expected,
    SOURCE, fixtures_path, fake_download, fake_grouped_cycles, start_year, end_year, fake_aggregated_version
)
from hestia_earth.aggregation.models.terms import aggregate
from hestia_earth.aggregation.cycle.utils import (
    AGGREGATION_KEYS, _update_cycle, _format_terms_results
)
from hestia_earth.aggregation.utils.quality_score import calculate_score

class_path = 'hestia_earth.aggregation.models.terms'


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
    expected_path = f"{fixtures_path}/cycle/terms/wheatGrain-aggregated.jsonld"
    with open(expected_path, encoding='utf-8') as f:
        expected = json.load(f)

    cycles = fake_grouped_cycles('wheatGrain')
    results = aggregate(AGGREGATION_KEYS, cycles)
    results = list(map(_format_terms_results, results))
    results = list(map(_update_cycle(None, start_year, end_year, SOURCE), results))
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
def test_aggregate_cycle_relative(*args):
    expected_path = f"{fixtures_path}/cycle/terms/relative-unit-aggregated.jsonld"
    with open(expected_path, encoding='utf-8') as f:
        expected = json.load(f)

    cycles = fake_grouped_cycles('relative-unit', is_relative=True)
    results = aggregate(AGGREGATION_KEYS, cycles)
    results = list(map(_format_terms_results, results))
    results = list(map(_update_cycle(None, start_year, end_year, SOURCE, False), results))
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
    expected_path = f"{fixtures_path}/cycle/terms/bananaFruit-aggregated.jsonld"
    with open(expected_path, encoding='utf-8') as f:
        expected = json.load(f)

    cycles = fake_grouped_cycles('bananaFruit')
    results = aggregate(AGGREGATION_KEYS, cycles)
    results = list(map(_format_terms_results, results))
    results = list(map(_update_cycle(None, start_year, end_year, SOURCE), results))
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
def test_aggregate_cycle_multiple_dates(*args):
    expected_path = f"{fixtures_path}/cycle/terms/multiple-dates.jsonld"
    with open(expected_path, encoding='utf-8') as f:
        expected = json.load(f)

    cycles = fake_grouped_cycles('multiple-dates')
    results = aggregate(AGGREGATION_KEYS, cycles)
    results = list(map(_format_terms_results, results))
    results = list(map(_update_cycle(None, start_year, end_year, SOURCE), results))
    results = list(map(calculate_score, results))
    results = results
    overwrite_expected(expected_path, results)
    assert results == expected
