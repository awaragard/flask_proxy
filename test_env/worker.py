import logging
from subprocess import Popen, PIPE, STDOUT

import os
import shutil
import yaml
from distutils.dir_util import copy_tree
from os.path import dirname, join

from test_env.resources import get_ust_exe
from test_env.test_cases import get_test_def


class TestSync():

    def __init__(self, name, test_dir):
        test_def = get_test_def(name)
        self.source_dir = dirname(test_def)
        self.test_dir = test_dir
        self.logger = logging.getLogger()
        self.sync_logger = logging.getLogger("test")

        with open(test_def) as file:
            cfg = yaml.safe_load(file)
            self.sync_args = cfg.get('sync_args') or ""
            self.assertions = cfg.get('assertions') or ""
            self.root_config = cfg.get('root_config') or "user-sync-config.yml"

    def run_test(self):
        copy_tree(self.source_dir, self.test_dir)
        shutil.copy(get_ust_exe(), join(self.test_dir, 'ust'))

        command = "ust -c {cfg} {args}".format(
            cfg=self.root_config,
            args=self.sync_args
        )

        results = []

        os.chdir(self.test_dir)
        p = Popen(command.split(" "), stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        for line in iter(p.stdout.readline, b''):
            line = decode(line)
            self.sync_logger.info(line)
            results.append(line)

        pass
        # self.prepare()
        # self.log_test_info(options)
        #
        #
        # os.chdir(self.test_dir)
        #
        # try:
        #     os.system(options['run_command'])
        # except os.error:
        #     pass
        #
        # results = read_data(options['log_file_path'])
        # os.chdir(self.base_dir)
        #
        # for line in results:
        #     self.logger.info(line, quiet=True)
        #
        # if self.check_results and not self.record:
        #     self.validate_results(options['assertions'], results)
        #
        # if self.record:
        #     c = Capture(self.record, test_config_path, options['components'])
        #     c.analyze(data=results)

def decode(text):
    try:
        text = text.decode()
    except:
        pass
    return str(text).strip()