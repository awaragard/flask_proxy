import logging
from subprocess import Popen, PIPE, STDOUT

import os
import re
import shutil
import yaml
from distutils.dir_util import copy_tree
from os.path import dirname, join
from pytest import fail

from test_env.resources import get_ust_exe
from test_env.test_cases import get_test_def

# These are errors we do not care about in a normal sync, so will
# always be part of our skipped errors
default_skipped_errors = [
    'success, error',
    'UMAPI timeout',
    'Next retry in'
]


class TestSync():

    def __init__(self, name, test_dir):
        test_def = get_test_def(name)
        self.test_name = name
        self.source_dir = dirname(test_def)
        self.test_dir = str(test_dir)
        self.logger = logging.getLogger()
        self.sync_logger = logging.getLogger("test")
        self.sync_results = []

        with open(test_def) as file:
            cfg = yaml.safe_load(file)
            self.sync_args = cfg.get('sync_args', '')
            self.assertions = cfg.get('assertions', '').splitlines()
            self.root_config = cfg.get('root_config', 'user-sync-config.yml')
            self.fail_on_error = bool(cfg.get('fail_on_error', True))
            self.allowed_errors = cfg.get('allowed_errors') or []
            self.allowed_errors.extend(default_skipped_errors)

    def run_sync(self):
        self.log_start()

        # prepare test directory
        copy_tree(self.source_dir, self.test_dir)
        shutil.copy(get_ust_exe(), join(self.test_dir, 'ust'))

        # Use CHDIR intentionally so the UST can resolve relative paths for CSV, etc
        # Absolute paths preferred, but this will not work in every case without updating config for test dir
        os.chdir(self.test_dir)
        command = "./ust -c {0} {1}".format(self.root_config, self.sync_args)
        p = Popen(command.split(" "), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        for line in iter(p.stdout.readline, b''):
            line = self.normalize(line)
            self.sync_logger.info(line)
            self.sync_results.append(line)

    def validate_results(self):
        """
        Check first for actual sync errors, and then verify that our asserted lines are present in sync.
        :return:
        """

        for i, l in enumerate(self.sync_results):
            for a in self.assertions:
                if self.normalize(a) in l:
                    self.assertions.remove(a)

            if self.fail_on_error:
                if re.search('(ERROR)|(CRITICAL)|(EXCEPTION)|(WARNING)', l, flags=re.IGNORECASE):
                    if not True in {self.normalize(s) in self.normalize(l) for s in self.allowed_errors}:
                        fail(l)

        if self.assertions:
            fail("Assertions not found in results: {}".format(self.assertions))

    def log_start(self):
        self.logger.info(
            "\n========================== Begin test: [{}] =========================="
                .format(self.test_name))
        self.logger.info("Using: " + os.path.abspath(self.root_config))
        self.logger.info("CLI args: " + self.sync_args)
        self.logger.info("Assertions: \n" + "\n".join(self.assertions))

    def normalize(self, text):
        try:
            text = text.decode()
        except:
            pass
        return str(text).strip().lower()
