import logging
import threading

import os
import requests
import vcr
import yaml
from flask import Flask
from requests import ConnectTimeout
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

from flask_proxy import view, error, config, resources

config.init_logger(resources.get_resource('logging_config.yml'))


class ProxyServer(threading.Thread):

    def __init__(self,
                 config_filename=None,
                 base_url=None,
                 protocol=None,
                 port=None,
                 cassette_dir=None,
                 record_mode=None,
                 match_on=None,
                 vcr_enabled=None,
                 log_level=None,
                 base_url_dict=None):
        super().__init__()

        file_opts = {}
        invoc_opts = {}
        if config_filename:
            logging.getLogger().info("Reading proxy configuration from: {}".format(config_filename))
            with open(config_filename, 'r') as f:
                file_opts.update(yaml.safe_load(f))


        self.config_filename = invoc_opts['config_filename'] = config_filename
        self.base_url = invoc_opts['base_url'] = base_url or file_opts.get('base_url')
        self.protocol = invoc_opts['protocol'] = protocol or file_opts.get('protocol', 'https')
        self.port = invoc_opts['port'] = port or file_opts.get('port', 8080)
        self.record_mode = invoc_opts['record_mode'] = record_mode or file_opts.get('record_mode', 'once')
        self.cassette_dir = invoc_opts['cassette_dir'] = cassette_dir or file_opts.get('cassette_dir', 'cassettes')
        self.vcr_enabled = invoc_opts['vcr_enabled'] = vcr_enabled or file_opts.get('vcr_enabled', True)
        self.match_on = invoc_opts['match_on'] = match_on or file_opts.get('match_on') or ['uri', 'method', 'raw_body']
        self.log_level = invoc_opts['log_level'] = log_level or file_opts.get('log_level', logging.DEBUG)
        self.host = invoc_opts['host'] = '{}://localhost:{}'.format(self.protocol, self.port)
        self.daemon = True
        self.invoc_opts = invoc_opts

        self.vcr = vcr.VCR(
            record_mode=self.record_mode,
            cassette_library_dir=self.cassette_dir,
            match_on=self.match_on,
            decode_compressed_response=True
        )

        logging.getLogger().setLevel(self.log_level)
        self.logger = view.logger = logging.getLogger("proxy")
        self.logger.info("Initialized with options: {}".format(invoc_opts))
        view.proxy_server = self
        error.register(view)

        self.application = Flask(self.name)
        self.application.url_map.strict_slashes = False
        self.application.config.update(os.environ)
        self.application.register_blueprint(view.view)

    def start_server(self):
        self.logger.info("Starting server")
        self.application.run(
            port=self.port,
            debug=False,
            use_reloader=False,
            ssl_context='adhoc' if self.protocol == "https" else None
        )

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
