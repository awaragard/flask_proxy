import logging
import logging.config
import os
from os.path import dirname, realpath, join

import vcr
from qconf import QConfig, parse_path


class ProxyConfig():
    def __init__(self, config_file=None):
        self.vcr = None
        self.base_url = None
        self.vcr_opts = None
        self.logger = logging.getLogger("proxy")

        if config_file:
            self.load_file(config_file)

    def load_file(self, path):

        self.logger.info("Reading proxy configuration from: {}".format(path))
        options = QConfig.from_yaml(path)
        self.base_url = options.get_string("base_url", required=True)
        self.protocol = options.get_string("protocol", "https")
        vcr_config = options.get_sub_config("vcr")
        self.config_root = dirname(realpath(path))
        cassette_dir = vcr_config.get_string("cassette_dir", "cassettes")
        if not os.path.isabs(cassette_dir):
            cassette_dir = join(self.config_root, cassette_dir)
        cassette_dir = parse_path(cassette_dir)

        self.vcr_enabled = vcr_config.get_bool("enabled")
        self.vcr_opts = {
            'record_mode': vcr_config.get_string("record_mode", "once"),
            'match_on': vcr_config.get_list("match_on", ['uri', 'method', 'raw_body']),
            'cassette_library_dir': cassette_dir
        }

        self.vcr = vcr.VCR(**self.vcr_opts)
        init_opts = {'protocol': self.protocol, 'base_url': self.base_url,
                     'config_root': self.config_root, 'vcr_opts': self.vcr_opts}
        self.logger.info("Initialized with options: {}".format(init_opts))


def init_logger(logging_config):
    logs_root = logging_config.get('logs_root', 'logs')
    for k, h in logging_config['handlers'].items():
        filename = h.get('filename')
        if filename:
            filename = parse_path(filename)
            if not filename == os.path.abspath(filename):
                filename = os.path.join(logs_root, filename)
            h['filename'] = filename
            log_dir = os.path.dirname(filename)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
    logging.config.dictConfig(logging_config)
