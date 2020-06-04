import subprocess
import sys

import os
import pytest
import requests

from flask_proxy import ProxyServer
from test.resources import get_resource

# from python_hosts import Hosts, HostsEntry

global gps

test_headers = {'User-Agent': 'none'}
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
    opts['cassette_dir'] = 'cassettes/' + str(test_name)
    return opts


def test_simple(proxy_server):
    opts = get_opts(get_name())

    opts['base_url_dict'] = {
        '/employees': 'dummy.restapiexample.com',
    }

    p = proxy_server(opts)

    resp = requests.get(p.host + '/api/v1/employees', headers=test_headers)
    assert resp.status_code == 200
    resp = requests.get(p.host + '/api/v1/badurl')
    assert resp.status_code == 417


def test_ust_delete(capsys):
    exe_path = get_resource("user-sync.exe")
    test_path = get_resource("delete")
    os.chdir(test_path)
    result = subprocess.check_output(exe_path)
    with capsys.disabled():
        print(result.decode())


def test_ust_simple(capsys):
    exe_path = get_resource("user-sync.exe")
    test_path = get_resource("simple_csv")

    os.chdir(test_path)
    result = subprocess.check_output(exe_path)
    with capsys.disabled():
        print(result.decode())


def test_ust_proxy(proxy_server, capsys):
    opts = get_opts(get_name())
    opts['base_url'] = "usermanagement-stage.adobe.io"
    opts['protocol'] = "https"
    opts['base_url_dict'] = {
        '/ims/exchange/jwt': 'ims-na1-stg1.adobelogin.com'
    }

    opts['mock_response_dict'] = {
        '/ims/exchange/jwt': {
            'status_code': 200,
            'body':{
                'expires_in': 10000,
                'access_token': "x"
            }
        },
    }

    proxy_server(opts)
    exe_path = get_resource("user-sync.exe")
    test_path = get_resource("proxy_csv")

    # r = requests.post("https://localhost:8083/ims/exchange/jwt", verify=False)
    #
    # z = r.json()
    #
    # #self.set_expiry(r.json()['expires_in'])
    #
    # #return r.json()['access_token']



    os.chdir(test_path)
    result = subprocess.check_output(exe_path)
    with capsys.disabled():
        print(result.decode())
