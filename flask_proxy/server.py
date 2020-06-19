import inspect
import logging
import threading
from enum import Enum

import os
import requests
import vcr
import yaml
from flask import Flask
from requests import ConnectTimeout
from urllib3.exceptions import InsecureRequestWarning

from flask_proxy.modes import VCRMode

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
                 log_level=None,
                 base_url_dict=None,
                 mock_response_dict=None, ):

        defaults, args = self.build_args_dict(locals())
        super().__init__()

        options = {}
        invoc_opts = {}
        if config_filename:
            logging.getLogger().info("Reading proxy configuration from: {}".format(config_filename))
            with open(config_filename, 'r') as f:
                options.update(yaml.safe_load(f))

        # Now override with named parameters and merge with defaults
        options.update(args)
        defaults.update(options)
        options = defaults


        #self.base_url = invoc_opts['base_url'] = base_url or file_opts.get('base_url')

        self.protocol = invoc_opts['protocol'] = protocol or options.get('protocol', 'https')
        self.port = invoc_opts['port'] = port or options.get('port', 8080)
        self.log_level = invoc_opts['log_level'] = log_level or options.get('log_level', logging.DEBUG)
        self.base_url_dict = invoc_opts['base_url_dict'] = base_url_dict or options.get('base_url_dict', {})
        self.mock_response_dict = invoc_opts['mock_response_dict'] = \
            mock_response_dict or options.get('mock_response_dict', {})

        self.host = invoc_opts['host'] = '{}://localhost:{}'.format(self.protocol, self.port)
        self.daemon = True
        self.invoc_opts = invoc_opts

        record_mode = invoc_opts['record_mode'] = record_mode or options.get('record_mode', 'all')
        cassette_dir = invoc_opts['cassette_dir'] = cassette_dir or options.get('cassette_dir', 'cassettes')
        match_on = invoc_opts['match_on'] = match_on or options.get('match_on') or ['uri', 'method', 'raw_body']
        self.mode = VCRMode.value_of(record_mode)
        self.vcr = vcr.VCR(
            record_mode=self.mode.value,
            cassette_library_dir=cassette_dir,
            match_on=match_on,
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

    def build_args_dict(self, all_locals):
        named_args = list(inspect.signature(self.__init__).parameters.values())
        non_default_args = {}
        default_args = {}
        for v in named_args:
            default_args[v.name] = v.default
            if v.name in all_locals and all_locals[v.name] != v.default:
                non_default_args[v.name] = all_locals[v.name]
        return default_args, non_default_args

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


