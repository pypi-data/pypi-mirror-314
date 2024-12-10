from hestia_earth.schema import MeasurementJSONLD, MeasurementStatsDefinition, MeasurementMethodClassification
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name

from . import _aggregated_version
from .term import should_aggregate


def _new_measurement(term: dict, value: float = None):
    node = MeasurementJSONLD().to_dict()
    node['term'] = linked_node(term)
    node['methodClassification'] = MeasurementMethodClassification.COUNTRY_LEVEL_STATISTICAL_DATA.value
    if value is not None:
        node['value'] = [value]
        node['statsDefinition'] = MeasurementStatsDefinition.SITES.value
    return _aggregated_version(node, 'term', 'methodClassification', 'statsDefinition', 'value')


def should_aggregate_measurement(measurement: dict):
    term = measurement.get('term', {})
    lookup = download_lookup(f"{term.get('termType')}.csv")
    value = get_table_value(lookup, 'termid', term.get('@id'), column_name('arrayTreatmentLargerUnitOfTime'))
    # ignore any measurement with time-split data
    return not value and should_aggregate(term)
