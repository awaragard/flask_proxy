import os

import requests
import pytest

from flask_proxy import ProxyServer

def test_simple():

    p = ProxyServer(
        base_url='dummy.restapiexample.com',
        protocol='http',
        port=8083,
        cassette_dir=os.getcwd() + '/test_simple/cassette',
        record_mode='once',
        vcr_enabled=True)

    p.start_async()
    resp = requests.get('http://localhost:8083/api/v1/employees')
    assert resp.status_code == 200

    p.shutdown()


    x = p.is_server_running()


    print()
