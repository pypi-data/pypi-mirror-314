from hestia_earth.schema import SchemaType, EmissionStatsDefinition
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.tools import flatten
from hestia_earth.utils.emission import cycle_emission_is_in_system_boundary

from hestia_earth.aggregation.utils import _aggregated_version, _unique_nodes
from hestia_earth.aggregation.utils.term import METHOD_MODEL
from hestia_earth.aggregation.utils.emission import get_method_tier


def _new_emission(cycle: dict):
    def emission(data: dict, value: float = None):
        term = data.get('term', {})
        nodes = data.get('nodes', [])
        # only add emissions included in the System Boundary
        if cycle_emission_is_in_system_boundary(cycle)(term.get('@id')):
            node = {'@type': SchemaType.EMISSION.value}
            node['term'] = linked_node(term)
            if value is not None:
                node['value'] = [value]
                node['statsDefinition'] = EmissionStatsDefinition.CYCLES.value
            node['methodModel'] = METHOD_MODEL
            node['methodTier'] = get_method_tier(nodes)
            inputs = flatten([n.get('inputs', []) for n in nodes])
            if len(inputs) > 0:
                node['inputs'] = list(map(linked_node, _unique_nodes(inputs)))
            # compute list of unique inputs, required for `background` emissions
            return _aggregated_version(node, 'term', 'statsDefinition', 'value', 'methodModel', 'methodTier')
    return emission
