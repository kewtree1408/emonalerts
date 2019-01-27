#!/usr/bin/env python

import unittest
from unittest.mock import (
    patch,
    Mock,
)

from emonalerts.schecker import get_failed_servers


class TestGetFailedServers(unittest.TestCase):
    # @patch('emonalert.schecker.requests.get', return_value=500)
    def test_get_failed_servers(self):
        servers = {
            'The Rosalind server': {
                'host': 'rosalind.info',
                'schemes': ['http', 'https']
            },
            'My Digital Ocean': {
                'host': 'vika.space',
                'ports': [80, 443]
            }
        }

        status_code = 500
        mock = Mock()
        mock.status_code = status_code
        with patch(
                'emonalerts.schecker.requests.get',
                return_value=mock,
        ) as mock_method:
            results = list(get_failed_servers(servers))

        expected_data = [
            ('http://rosalind.info', status_code),
            ('https://rosalind.info', status_code),
            ('http://vika.space', status_code),
            ('https://vika.space', status_code),
        ]
        self.assertEqual(sorted(results), sorted(expected_data))

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


# class TestCheck(unittest.TestCase):
#     def setUp(self):
#         self.parser = parse_args()
#         self.cur_dir = Path.cwd()

#     def test_check_successful(self):
#         self.setting_path = str(self.cur_dir.joinpath('src/tests/input/success_settings.toml'))
#         self.credential_path = str(self.cur_dir.joinpath('src/tests/input/success_creds.json'))

#     def test_check_without_owner(self):
#         self.setting_path = str(self.cur_dir.joinpath('src/tests/input/failed_settings.toml'))
#         self.credential_path = str(self.cur_dir.joinpath('src/tests/input/failed_creds.json'))
