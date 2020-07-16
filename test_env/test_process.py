import logging
import sys

import os
import pytest

from flask_proxy import VCRMode, ProxyServer
from flask_proxy.mock_response import MockResponse
from test_env import init_logger
from test_env.test_sync import TestSync

init_logger(logging.DEBUG)
logger = logging.getLogger()

root_dir = os.getcwd()

record_mode = False
check_results = True

test_headers = {'User-Agent': 'none'}



@pytest.fixture
def meta():
    yield
    os.chdir(root_dir)


def run(name, dir):
    test = TestSync(name, dir)
    test.run_sync()

    if check_results and not record_mode:
        test.validate_results()


class TestUST(object):

    def test_all_users(self, meta, tmpdir, start_proxy):

        prox = start_proxy(get_name(), VCRMode.record)

        run(get_name(), tmpdir)

    def test_all_users2(self, meta, tmpdir):
        run(get_name(), tmpdir)

def get_name():
    return sys._getframe(1).f_code.co_name
