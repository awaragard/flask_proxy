import pytest

from flask_proxy import ProxyServer, VCRMode
from flask_proxy.mock_response import MockResponse

mock_auth = MockResponse(
    method='POST',
    endpoint='/ims/exchange/jwt',
    body={
        'expires_in': 10000,
        'access_token': "x"
    })

test_opts = {
    'base_urls': 'usermanagement-stage.adobe.io',
    'protocol': 'https',
    'mode': VCRMode.record,
    'mock_responses': {mock_auth.endpoint: mock_auth}
}

def start_proxy(record_mode):
    opts = test_opts.copy()
    opts['cassette_dir'] = 'cassettes/default'
    opts['mode'] = record_mode
    gps = ProxyServer(**opts).start_async()
    return gps