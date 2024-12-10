from hestia_earth.schema import SchemaType
from hestia_earth.utils.api import find_node_exact
from hestia_earth.utils.model import linked_node
from hestia_earth.utils.tools import non_empty_list, flatten

from hestia_earth.aggregation.log import logger

HESTIA_BIBLIO_TITLE = 'Hestia: A harmonised way to represent, share, and analyse agri-environmental data'


def get_source():
    source = find_node_exact(SchemaType.SOURCE, {'bibliography.title': HESTIA_BIBLIO_TITLE})
    logger.debug('source=%s', source)
    return linked_node(source) if source else None


def format_aggregated_sources(nodes: list, node_key: str = 'source'):
    sources = non_empty_list(flatten([n.get('aggregatedSources', n.get(node_key)) for n in nodes]))
    return sorted(
        list(map(linked_node, [dict(t) for t in {tuple(d.items()) for d in sources}])),
        key=lambda x: x.get('@id')
    )
