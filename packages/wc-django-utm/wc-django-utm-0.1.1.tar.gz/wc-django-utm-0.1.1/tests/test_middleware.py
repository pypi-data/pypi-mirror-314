import pytest
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

from wcd_utm.middleware import UTMSessionMiddleware
from wcd_utm.conf import settings


@pytest.mark.django_db
def test_multiple_same_requests():
    url = '/?utm_content=5&utm_content=shaza&gclid=5'
    factory = RequestFactory()
    request = factory.get(url)
    md = UTMSessionMiddleware(lambda r: None)
    smd = SessionMiddleware(lambda r: None)

    smd.process_request(request)
    md(request)
    md(request)

    assert len(request.session[settings.SESSION_STORAGE_KEY]) == 1

    request1 = factory.get(url)
    request2 = factory.get('/path/to/something' + url + '&with=get&parameters')
    smd.process_request(request1)
    md(request1)
    request2.session = request1.session
    md(request2)

    assert len(request1.session[settings.SESSION_STORAGE_KEY]) == 1


@pytest.mark.django_db
def test_multiple_different_requests():
    url = '/?utm_content=5&utm_content=shaza&gclid=5'
    factory = RequestFactory()
    md = UTMSessionMiddleware(lambda r: None)
    smd = SessionMiddleware(lambda r: None)

    request1 = factory.get(url)
    request2 = factory.get(url + '&utm_content=third')
    smd.process_request(request1)
    md(request1)
    request2.session = request1.session
    md(request2)

    assert len(request1.session[settings.SESSION_STORAGE_KEY]) == 2
