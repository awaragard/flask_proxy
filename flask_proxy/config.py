import logging
import logging.config
import os

import vcr
import yaml


class ProxyOptions():
    def __init__(self,
                 base_url=None,
                 protocol='https',
                 port=8080,
                 cassette_dir='cassettes',
                 record_mode='once',
                 match_on=None,
                 vcr_enabled=True):
        self.base_url = base_url
        self.protocol = protocol
        self.port = port
        self.record_mode = record_mode
        self.cassette_dir = cassette_dir
        self.vcr_enabled = vcr_enabled
        self.match_on = match_on or ['uri', 'method', 'raw_body']
        self.logger = logging.getLogger("proxy")
        self.logger.info("Initialized with options: {}".format(vars(self)))

        self.vcr = vcr.VCR(
            record_mode=self.record_mode,
            cassette_library_dir=self.cassette_dir,
            match_on=self.match_on
        )


def init_logger(path):
    with open(path) as f:
        logging_config = yaml.safe_load(f)
    logs_root = logging_config.get('logs_root', 'logs')
    for k, h in logging_config['handlers'].items():
        filename = h.get('filename')
        if filename:
            if not filename == os.path.abspath(filename):
                filename = os.path.join(logs_root, filename)
            h['filename'] = filename
            log_dir = os.path.dirname(filename)
            if not os.path.exists(log_dir):
                os.makedirs(log_dir)
    logging.config.dictConfig(logging_config)
