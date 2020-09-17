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

record_mode = None
check_results = True

if record_mode is not None:
    prox = start_proxy(VCRMode.record if record_mode else VCRMode.playback)


def run(name, dir):
    try:

        test = TestSync(name, dir, record_mode)
        if record_mode is not None:
            prox.set_cassette_dir(test.source_dir)

        test.run_sync()

        if check_results and not record_mode:
            test.validate_results()
    finally:
        os.chdir(root_dir)


def get_name():
    return sys._getframe(1).f_code.co_name


class TestUST(object):

    # def test_setup_test_to_delete_all_users(self, tmpdir):
    #     run(get_name(), tmpdir)
    #
    # def test_setup_test_to_create_users(self, tmpdir):
    #     run(get_name(), tmpdir)

    def test_create_all_users(self, tmpdir):
        run(get_name(), tmpdir)

    def test_create_mapped_users(self, tmpdir):
        run(get_name(), tmpdir)

    def test_create_by_push_strategy(self, tmpdir):
        run(get_name(), tmpdir)

    def test_private_key_decryption(self, tmpdir):
        run(get_name(), tmpdir)

    def test_update_fname(self, tmpdir):
        run(get_name(), tmpdir)

    def test_update_lname(self, tmpdir):
        run(get_name(), tmpdir)

    def test_update_email(self, tmpdir):
        run(get_name(), tmpdir)

    def test_update_group(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_adobe_only_action_remove(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_adobe_only_action_remove_with_max_limit(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_adobe_only_action_delete(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_adobe_only_action_exclude(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_adobe_only_action_remove_adobe_groups(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_adobe_only_action_write_file(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_adobe_only_action_stray_list(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_adobe_only_action_stray_list_with_max_limit(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_exclude_adobe_groups(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_exclude_adobe_users(self, tmpdir):
        run(get_name(), tmpdir)

    def test_delete_exclude_identity_types(self, tmpdir):
        run(get_name(), tmpdir)

    def test_default_country_code(self, tmpdir):
        run(get_name(), tmpdir)

    def test_user_identity_type_enterpriseID(self, tmpdir):
        run(get_name(), tmpdir)

    def test_user_identity_type_adobeID(self, tmpdir):
        run(get_name(), tmpdir)

    def test_extension_config(self, tmpdir):
        run(get_name(), tmpdir)

    def test_multi_umapi_create(self, tmpdir):
        run(get_name(), tmpdir)

    def test_multi_umapi_adobe_only_action_remove(self, tmpdir):
        run(get_name(), tmpdir)

    def test_multi_umapi_adobe_only_action_delete(self, tmpdir):
        run(get_name(), tmpdir)

    def test_multi_umapi_adobe_only_action_stray_list(self, tmpdir):
        run(get_name(), tmpdir)

    def test_multi_umapi_create_groups(self, tmpdir):
        run(get_name(), tmpdir)

    def test_credentials_store(self, tmpdir):
        run(get_name(), tmpdir)

    def test_credentials_store_ldap(self, tmpdir):
        run(get_name(), tmpdir)

    def test_credentials_store_create_users(self, tmpdir):
        run(get_name(), tmpdir)

    def test_credentials_store_adobe_console(self, tmpdir):
        run(get_name(), tmpdir)

    def test_credentials_store_multi_umapi(self, tmpdir):
        run(get_name(), tmpdir)




