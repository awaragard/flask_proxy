import os

from flask_proxy import ProxyServer

p = ProxyServer(
    base_url='dummy.restapiexample.com',
    protocol='http',
    port=8083,
    cassette_dir=os.getcwd() + '/cassette',
    record_mode='once',
    vcr_enabled=True)

p.start_async()
print()
