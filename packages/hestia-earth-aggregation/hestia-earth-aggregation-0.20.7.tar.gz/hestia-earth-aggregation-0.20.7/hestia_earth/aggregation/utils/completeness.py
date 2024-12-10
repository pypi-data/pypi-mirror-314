from hestia_earth.schema import SchemaType, TermTermType, CompletenessField, COMPLETENESS_MAPPING

from .practice import is_complete as is_practice_complete


def blank_node_completeness_key(blank_node: dict):
    term_type = blank_node.get('term', {}).get('termType')
    return COMPLETENESS_MAPPING.get(blank_node.get('@type'), {}).get(term_type, term_type)


IS_COMPLETE = {
    CompletenessField.ANIMALFEED.value: lambda product: product.get('termType') in [
        TermTermType.ANIMALPRODUCT.value,
        TermTermType.LIVEANIMAL.value,
        TermTermType.LIVEAQUATICSPECIES.value
    ]
}
IS_TERM_TYPE_COMPLETE = {
    TermTermType.CROPRESIDUEMANAGEMENT.value: is_practice_complete,
    TermTermType.LANDCOVER.value: is_practice_complete,
    TermTermType.TILLAGE.value: is_practice_complete,
    TermTermType.WATERREGIME.value: is_practice_complete,
    TermTermType.LANDUSEMANAGEMENT.value: is_practice_complete
}
SKIP_COMPLETENESS = [SchemaType.MEASUREMENT.value, SchemaType.EMISSION.value]


def is_complete(node: dict, product: dict, blank_node: dict):
    completeness_key = blank_node_completeness_key(blank_node)
    return any([
        blank_node.get('@type') in SKIP_COMPLETENESS,
        # using an existing completeness key
        all([
            node.get('completeness', {}).get(completeness_key, False),
            IS_COMPLETE.get(completeness_key, lambda *args: True)(product)
        ]),
        # using a termType
        IS_TERM_TYPE_COMPLETE.get(completeness_key, lambda *args: False)(node, completeness_key)
    ])


def update_completeness(node: dict):
    return node | {
        'completeness': node.get('completeness') | {
            key: value(node, key) for key, value in IS_TERM_TYPE_COMPLETE.items()
        }
    } if 'completeness' in node else node


def group_completeness(completeness: dict, node: dict, product: dict):
    for key in node.get('completeness', {}).keys():
        is_complete = node.get('completeness').get(key, False)
        completeness[key] = completeness.get(key, 0) + (1 if is_complete else 0)
    return completeness
