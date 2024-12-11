from typing import *
from collections import OrderedDict

from .conf import settings


__all__ = 'QueryLists', 'resolve'

QueryLists = List[Tuple[str, List[str]]]
Resolved = Dict[str, List[str]]


def _merge_lists(current: Optional[List[str]], merge: List[str]):
    current = [] if current is None else current
    return current + [v for v in merge if v not in current]


def resolve(
    lists: QueryLists,
    parameters: Sequence[str] = settings.PARAMETERS,
    prefixes: Sequence[str] = settings.RESOLVABLE_PREFIXES,
) -> Resolved:
    match_prefixes = [(k, len(k)) for k in prefixes]
    parameters = tuple(parameters)
    merged = OrderedDict()

    for key, values in lists:
        prefix, l = next(
            (x for x in match_prefixes if key.startswith(x[0])),
            (None, 0)
        )

        if key in parameters or prefix is not None:
            merged[key] = _merge_lists(merged.get(key, None), values)

        if prefix is not None and settings.UNWRAP_PREFIXED_PARAMETERS:
            subkey = key[l:]

            if subkey not in parameters:
                merged[subkey] = _merge_lists(merged.get(subkey, None), values)

    return merged
