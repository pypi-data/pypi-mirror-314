from hestia_earth.schema import TermTermType
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import list_sum
from hestia_earth.utils.model import filter_list_term_type


def _is_organic(lookup, term_id: str):
    return get_table_value(lookup, 'termid', term_id, column_name('isOrganic')) == 'organic'


def is_organic(cycle: dict):
    term_type = TermTermType.STANDARDSLABELS
    lookup = download_lookup(f"{term_type.value}.csv")
    practices = filter_list_term_type(cycle.get('practices', []), term_type)
    return any([_is_organic(lookup, p.get('term', {}).get('@id')) for p in practices])


def _is_irrigated(lookup, term_id: str):
    return get_table_value(lookup, 'termid', term_id, column_name('irrigated'))


def is_irrigated(cycle: dict):
    term_type = TermTermType.WATERREGIME
    lookup = download_lookup(f"{term_type.value}.csv")
    practices = filter_list_term_type(cycle.get('practices', []), term_type)
    return any([
        list_sum(p.get('value', []), 0) > 0 for p in practices if _is_irrigated(lookup, p.get('term', {}).get('@id'))
    ])
