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

@pytest.fixture()
def start_proxy():
    def _start_proxy(test_name, record_mode):
        opts = test_opts.copy()
        opts['cassette_dir'] = 'cassettes/' + str(test_name)
        opts['mode'] = record_mode

        global gps
        gps = ProxyServer(**opts).start_async()
        return gps

    yield _start_proxy
    gps.shutdown()

