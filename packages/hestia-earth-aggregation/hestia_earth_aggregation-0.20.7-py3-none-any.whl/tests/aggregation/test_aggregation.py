from unittest.mock import patch

from tests.utils import PRODUCT_BY_FILENAME, SOURCE, WORLD
from hestia_earth.aggregation import aggregate

class_path = 'hestia_earth.aggregation'


@patch(f"{class_path}.find_nodes")
@patch(f"{class_path}.aggregate_global", return_value={})
def test_aggregate(mock_aggregate, mock_find_nodes):
    product = PRODUCT_BY_FILENAME['wheatGrain']

    # without nodes
    mock_find_nodes.return_value = []
    aggregate(WORLD, product, 2000, 2009, SOURCE)
    mock_aggregate.assert_not_called()

    # with nodes
    mock_find_nodes.return_value = [{}]
    aggregate(WORLD, product, 2000, 2009, SOURCE)
    mock_aggregate.assert_called_once()
