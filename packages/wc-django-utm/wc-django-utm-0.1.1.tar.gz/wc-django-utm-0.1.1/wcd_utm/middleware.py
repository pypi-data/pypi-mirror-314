import logging

from .shortcuts import resolve_from_request
from . import session_storage


logger = logging.getLogger(__name__)


class UTMSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            session_storage.put(request.session, resolve_from_request(request))
        except Exception as e:
            logging.exception(e, exc_info=True)

        response = self.get_response(request)
        return response
