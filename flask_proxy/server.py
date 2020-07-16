import logging
import threading

import os
import requests
import vcr
import yaml
from flask import Flask
from requests import ConnectTimeout
from urllib3.exceptions import InsecureRequestWarning

from flask_proxy import view, error, config, resources
from flask_proxy.mock_response import MockResponse
from flask_proxy.modes import VCRMode

config.init_logger(resources.get_resource('logging_config.yml'))
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class ProxyServer(threading.Thread):

    def __init__(self,
                 base_urls=None,
                 protocol=None,
                 port=8083,
                 cassette_dir='cassettes',
                 mode=VCRMode.record,
                 match_on=None,
                 log_level=logging.DEBUG,
                 mock_responses=None,
                 **kwargs
                 ):

        super().__init__()
        logging.getLogger().setLevel(log_level or logging.DEBUG)

        # base_urls is a mapping of endpoints to domains.  Default will be the fallback always
        # If we get a string, this becomes the default.  If we get a collection, we use that instead
        base_urls = base_urls or {}
        self.base_urls = {}
        if isinstance(base_urls, str):
            self.add_base_url('default', base_urls)
        else:
            self.base_urls.update(base_urls)

        self.port = port
        self.mode = mode if isinstance(mode, VCRMode) else VCRMode.value_of(mode)
        self.protocol = protocol
        self.mock_responses = mock_responses or {}
        self.host = '{}://localhost:{}'.format(self.protocol, self.port)
        self.options = {k: v for k, v in vars(self).items() if not k.startswith("_")}
        self.logger = view.logger = logging.getLogger("proxy")
        self.logger.info("Initializing with options: {}".format(self.options))

        self.vcr = vcr.VCR(
            record_mode=self.mode.value,
            cassette_library_dir=os.path.abspath(cassette_dir),
            match_on=match_on or ['uri', 'method', 'raw_body'],
            decode_compressed_response=True
        )


        # Configure app and views
        view.proxy_server = self
        error.register(view)
        self.daemon = True
        self.application = Flask(self.name)
        self.application.url_map.strict_slashes = False
        self.application.config.update(os.environ)
        self.application.register_blueprint(view.view)

    def add_base_url(self, endpoint, url):
        self.base_urls[endpoint] = url

    def add_mock_response(self, endpoint, response):
        self.mock_responses[endpoint] = response

    def get_base_url(self, endpoint=None):
        if endpoint:
            for k, v in self.base_urls.items():
                if endpoint.startswith(k):
                    return v
        return self.base_urls['default']

    def get_mock_response(self, endpoint):
        for k, v in self.mock_responses.items():
            if endpoint.startswith(k):
                if not isinstance(v, MockResponse):
                    raise ValueError("Mock response for '{}' should be of type MockResponse.  "
                                     "Instead, got '{}'".format(k, type(v)))
                return v.to_flask_response()

    def set_mode(self, mode):
        if not isinstance(mode, VCRMode):
            raise ValueError("Invalid mode: {}.  Please use VCRMode enum.".format(mode))
        self.mode = mode
        self.vcr.record_mode = mode.value

    def start_server(self):
        self.logger.info("Starting server")
        self.application.run(
            port=self.port,
            debug=False,
            use_reloader=False,
            ssl_context='adhoc' if self.protocol == "https" else None
        )

    @classmethod
    def from_file(cls, config_filename):
        with open(config_filename, 'r') as f:
            options = (yaml.safe_load(f))
            return ProxyServer(**options)

    def run(self):
        try:
            self.start_server()
        except RuntimeError:
            pass

    def start_sync(self):
        self.start_server()

    def start_async(self):
        self.start()
        return self

    def shutdown(self):
        requests.get(self.host + '/shutdown', verify=False)

    def is_server_running(self):
        try:
            requests.get(self.host + '/ping', timeout=2, verify=False)
            return True
        except ConnectTimeout:
            return False
