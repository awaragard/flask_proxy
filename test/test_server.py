import sys

import pytest
import requests

from flask_proxy import ProxyServer

global gps

test_opts = {
    'base_url': 'dummy.restapiexample.com',
    'protocol': 'http',
    'port': 8083,
    'cassette_dir': None,
    'record_mode': 'once',
    'vcr_enabled': True,
    'log_level': 'INFO'
}


# noinspection PyUnboundLocalVariable
@pytest.fixture()
def proxy_server():
    def _proxy_server(opts):
        global gps
        gps = ProxyServer(**opts).start_async()
        return gps
    yield _proxy_server
    gps.shutdown()

def get_name():
    return sys._getframe(1).f_code.co_name

def get_opts(test_name):
    opts = test_opts.copy()
    opts['cassette_dir'] = 'cassette/' + str(test_name)
    return opts


def test_simple(proxy_server):
    opts = get_opts(get_name())
    p = proxy_server(opts)
    resp = requests.get(p.host + '/api/v1/employees')
    assert resp.status_code == 200
    resp = requests.get(p.host + '/api/v1/badurl')
    assert resp.status_code == 417



