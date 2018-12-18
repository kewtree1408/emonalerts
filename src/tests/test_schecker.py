#!/usr/bin/env python

import unittest

class TestConfig(unittest.TestCase):
    def test_empty_config(self):


    def test_simple_config(self):
        pass

    def test_bad_config(self):
        pass


class TestHostSettings(unittest.TestCase):

    def test_host_settings(self):
        pass

    def test_incorrect_host_settings(self):
        pass


class TestGetFailedServers(unittest.TestCase):

    def test_get_failed_servers(self):
        pass

    def test_get_failed_servers_without_name(self):
        pass

    def test_get_failed_servers_with_400(self):
        pass

    def test_get_failed_servers_with_500(self):
        pass

    def test_get_failed_servers_with_timeout(self):
        pass

    def test_get_failed_servers_with_connection_error(self):
        pass

    def test_get_failed_servers_with_some_expection(self):
        pass

    def test_get_failed_servers_without_failures(self):
        pass


class TestHaveToSendAlert(unittest.TestCase):

    def test_have_to_send_alert_file_with_zero(self):
        pass

    def test_have_to_send_alert_file_with_not_zero(self):
        pass

    def test_have_to_send_alert_file_not_found(self):
        pass


class TestCheck(unittest.TestCase):

    def setUp(self):
        self.parser = parse_args()
        self.cur_dir = Path.cwd()

    def test_check_successful(self):
        self.setting_path = str(self.cur_dir.joinpath('src/tests/input/success_settings.toml'))
        self.credential_path = str(self.cur_dir.joinpath('src/tests/input/success_creds.json'))


    def test_check_without_owner(self):
        self.setting_path = str(self.cur_dir.joinpath('src/tests/input/failed_settings.toml'))
        self.credential_path = str(self.cur_dir.joinpath('src/tests/input/failed_creds.json'))


