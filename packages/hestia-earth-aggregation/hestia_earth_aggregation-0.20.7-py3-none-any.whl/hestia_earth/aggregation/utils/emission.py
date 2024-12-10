from hestia_earth.schema import EmissionMethodTier
_DEFAULT_TIER = EmissionMethodTier.TIER_1.value


def get_method_tier(emissions: list):
    values = set([e.get('methodTier', _DEFAULT_TIER) for e in emissions])
    return list(values)[0] if len(values) == 1 else _DEFAULT_TIER
