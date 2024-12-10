from unittest.mock import patch

from tests.utils import TERM, fake_aggregated_version
from hestia_earth.aggregation.cycle.practice import _new_practice

class_path = 'hestia_earth.aggregation.cycle.practice'


@patch(f"{class_path}._aggregated_version", side_effect=fake_aggregated_version)
@patch(f"{class_path}.download_hestia", return_value=TERM)
def test_new_practice(*args):
    # with a Term as string
    practice = _new_practice('term')
    assert practice == {
        '@type': 'Practice',
        'term': TERM
    }

    # with a Term as dict
    practice = _new_practice({'term': TERM}, 10)
    assert practice == {
        '@type': 'Practice',
        'term': TERM,
        'value': [10],
        'statsDefinition': 'cycles'
    }
