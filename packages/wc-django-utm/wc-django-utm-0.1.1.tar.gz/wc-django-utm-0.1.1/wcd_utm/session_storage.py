from typing import *
from django.contrib.sessions.backends.base import SessionBase
from django.utils import timezone

from .resolver import Resolved

from .conf import settings


__all__ = 'put', 'clear',

Stored = List[Tuple[str, Resolved]]


def put(session: SessionBase, params: Resolved) -> bool:
    if not params:
        return False

    storage_key = settings.SESSION_STORAGE_KEY
    access_key = settings.SESSION_ACCESS_KEY
    session.setdefault(storage_key, [])
    session.setdefault(access_key, {})

    storage = session[storage_key]

    if storage:
        _, latest = storage[-1]

        if latest == params:
            return False

    timestamp = timezone.now().isoformat()
    storage.append((timestamp, params))
    session[access_key] = params

    session.modified = True

    return True


def clear(session: SessionBase) -> Stored:
    session.pop(settings.SESSION_ACCESS_KEY)
    return session.pop(settings.SESSION_STORAGE_KEY, [])
