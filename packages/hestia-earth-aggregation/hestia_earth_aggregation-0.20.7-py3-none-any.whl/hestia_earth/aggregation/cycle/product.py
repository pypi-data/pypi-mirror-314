from hestia_earth.schema import SchemaType, ProductStatsDefinition
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version


def _new_product(data: dict, value: float = None):
    node = {'@type': SchemaType.PRODUCT.value}
    term = data.get('term')
    node['term'] = linked_node(term)
    if value is not None:
        node['value'] = [value]
        node['statsDefinition'] = ProductStatsDefinition.CYCLES.value
        if data.get('economicValueShare'):
            node['economicValueShare'] = data.get('economicValueShare')
    return _aggregated_version(node, 'term', 'statsDefinition', 'value')
