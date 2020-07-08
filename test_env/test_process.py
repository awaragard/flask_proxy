import logging
import sys

import os
import pytest

from test_env import init_logger
from test_env.worker import TestSync

init_logger(logging.DEBUG)
logger = logging.getLogger()

root_dir = os.getcwd()

@pytest.fixture
def meta(tmpdir):
    yield
    os.chdir(root_dir)



def run(name, dir):
    log_test_info(name)
    ts = TestSync(name, dir)
    ts.run_test()

class TestUST(object):

    def test_all_users(self, meta, tmpdir):
        run(get_name(), "C:\\ZZ")


def clean_console():
    pass


def get_name():
    return sys._getframe(1).f_code.co_name


def log_test_info(test_name):
    divider = "=========================="
    header = divider + " {0} " + divider
    logger.info("\n" + header.format("Running test: " + test_name) + "\n")


def test_cleanup():
    clean_console()

# @pytest.fixture()
# def runner(tmpdir):
#     if not default_options['test_mode']:
#         clean_console()
#     default_options['test_dir'] = tmpdir
#     yield TestRunner(**default_options)
#     shutil.rmtree(tmpdir)


