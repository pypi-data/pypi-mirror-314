from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import filter_list_term_type

from .blank_node import filter_blank_nodes


_PRACTICE_AGGREGATE_COMPLETE_TERM_TYPES = [
    TermTermType.CROPRESIDUEMANAGEMENT.value,
    TermTermType.LANDCOVER.value,
    TermTermType.TILLAGE.value,
    TermTermType.WATERREGIME.value
]
_PRACTICE_AGGREGATE_DEFAULT_TERM_TYPES = [
    TermTermType.LANDUSEMANAGEMENT.value
]


def is_complete(node: dict, term_type: str):
    practices = filter_list_term_type(node.get('practices', []), [term_type])
    return term_type not in _PRACTICE_AGGREGATE_COMPLETE_TERM_TYPES or len(filter_blank_nodes(practices)) > 0


def filter_practices(practices: list, start_year: int, end_year: int):
    return filter_blank_nodes(
        filter_list_term_type(practices, _PRACTICE_AGGREGATE_COMPLETE_TERM_TYPES), start_year, end_year
    ) + [
        p for p in filter_list_term_type(practices, _PRACTICE_AGGREGATE_DEFAULT_TERM_TYPES)
        if p.get('term', {}).get('units') in ['ratio', 'number', 'days']
    ]
