import urllib.parse
import json
from django.http import HttpRequest, QueryDict

from .conf import settings
from . import resolver


__all__ = (
    'resolve_from_url',
    'resolve_from_dict',
    'resolve_from_request',
)


def resolve_from_url(url: str, **kwargs):
    url = urllib.parse.urlparse(url)
    query_dict = QueryDict(url.query)

    return resolver.resolve(query_dict.lists(), **kwargs)


def resolve_from_dict(values: dict, **kwargs):
    return resolver.resolve(
        [
            (key, (
                list(value)
                if isinstance(value, (list, tuple, set)) else
                [value]
            ))
            for key, value in values.items()
        ],
        **kwargs,
    )


def resolve_from_request(request: HttpRequest, **kwargs):
    if settings.HEADER_ORIGIN_URL in request.META:
        return resolve_from_url(
            request.META[settings.HEADER_ORIGIN_URL], **kwargs
        )

    if settings.HEADER_JSON in request.META:
        return resolve_from_dict(
            json.loads(request.META[settings.HEADER_JSON]), **kwargs
        )

    return resolver.resolve(request.GET.lists(), *kwargs)
