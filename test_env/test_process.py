import logging
import sys

import os

from flask_proxy import VCRMode
from test_env import init_logger
from test_env.conftest import start_proxy
from test_env.test_sync import TestSync

init_logger(logging.DEBUG)
logger = logging.getLogger()
root_dir = os.getcwd()

record_mode = True
check_results = True

#prox = start_proxy(VCRMode.record if record_mode else VCRMode.playback)


def run(name, dir):
    try:
        test = TestSync(name, dir)
        #prox.set_cassette_dir(test.source_dir)

        test.run_sync()

        if check_results and not record_mode:
            test.validate_results()
    finally:
        os.chdir(root_dir)


def get_name():
    return sys._getframe(1).f_code.co_name


class TestUST(object):

    def test_all_users(self, tmpdir):
        run(get_name(), tmpdir)
