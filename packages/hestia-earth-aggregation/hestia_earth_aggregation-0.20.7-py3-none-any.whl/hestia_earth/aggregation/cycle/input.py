from hestia_earth.schema import SchemaType, InputStatsDefinition
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version


def _new_input(data: dict, value: float = None):
    node = {'@type': SchemaType.INPUT.value}
    term = data.get('term')
    node['term'] = linked_node(term)
    if value is not None:
        node['value'] = [value]
        node['statsDefinition'] = InputStatsDefinition.CYCLES.value
    return _aggregated_version(node, 'term', 'statsDefinition', 'value')
