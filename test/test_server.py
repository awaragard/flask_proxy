import subprocess
import sys

import os
import pytest

from flask_proxy import ProxyServer, VCRMode
from flask_proxy.mock_response import MockResponse
from test.resources import get_resource

global gps

test_headers = {'User-Agent': 'none'}

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
    opts['cassette_dir'] = 'cassettes/' + str(test_name)
    return opts


# def test_simple(proxy_server):
#     opts = get_opts(get_name())
#     p = proxy_server(opts)
#
#     resp = requests.get(p.host + '/api/v1/employees', headers=test_headers)
#     assert resp.status_code == 200
#     resp = requests.get(p.host + '/api/v1/badurl')
#     assert resp.status_code == 417


def test_ust_delete(capsys):
    exe_path = get_resource("user-sync.exe")
    test_path = get_resource("delete")
    os.chdir(test_path)
    result = subprocess.check_output(exe_path)
    with capsys.disabled():
        print(result.decode())


def test_ust_proxy(proxy_server, capsys):
    opts = get_opts(get_name())

    proxy_server(opts)
    exe_path = get_resource("user-sync.exe")
    test_path = get_resource("proxy_csv")

    os.chdir(test_path)
    result = subprocess.check_output(exe_path)
    with capsys.disabled():
        print(result.decode())
