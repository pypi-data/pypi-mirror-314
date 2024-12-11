import pytest
from django.test import RequestFactory

from wcd_utm import resolver
from wcd_utm.shortcuts import resolve_from_request, resolve_from_url
from wcd_utm.conf import settings


@pytest.mark.django_db
def test_default_parameters_resolver():
    url = '/?utm_content=5&utm_content=shaza&gclid=5'
    request = RequestFactory().get(url)
    resolved = resolver.resolve(request.GET.lists())

    assert resolved == resolve_from_request(request)
    assert resolved == resolve_from_url(url)

    assert resolved['gclid'] == ['5']
    assert resolved['utm_content'] == ['5', 'shaza']
    assert 'content' not in resolved
    assert len(resolved) == 2


@pytest.mark.django_db
def test_url_header():
    url = '/?utm_content=5&utm_content=shaza&gclid=5'
    request = RequestFactory().get(
        url, **{settings.HEADER_ORIGIN_URL: url + '&gclid=6'}
    )
    resolved = resolver.resolve(request.GET.lists())
    request_resolved = resolve_from_request(request)

    assert resolved != request_resolved
    assert request_resolved['gclid'] == ['5', '6']

    url = '/?utm_content=5&utm_content=shaza&gclid=5'
    request = RequestFactory().get(
        url, **{settings.HEADER_ORIGIN_URL: '/?gclid=6'}
    )
    resolved = resolver.resolve(request.GET.lists())
    request_resolved = resolve_from_request(request)

    assert resolved != request_resolved
    assert request_resolved['gclid'] == ['6']
    assert len(request_resolved) == 1


@pytest.mark.django_db
def test_json_header():
    url = '/?utm_content=5&utm_content=shaza&gclid=5'
    request = RequestFactory().get(
        url, **{settings.HEADER_JSON: '{"gclid": 8, "alambalam": "7"}'}
    )
    resolved = resolver.resolve(request.GET.lists())
    request_resolved = resolve_from_request(request)

    assert resolved != request_resolved
    assert request_resolved['gclid'] == [8]
    assert len(request_resolved) == 1
