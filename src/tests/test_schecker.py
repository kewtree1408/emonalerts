#!/usr/bin/env python

import unittest
from unittest.mock import (
    patch,
    Mock,
)

from emonalerts.schecker import get_failed_servers
import responses
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
)


class TestGetFailedServers(unittest.TestCase):
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

        status_code = 404
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
        servers = {
            'The Rosalind server': {
                'schemes': ['http', 'https']
            },
            'My Digital Ocean': {
                'ports': [80, 443]
            }
        }
        results = list(get_failed_servers(servers))

        expected_data = []
        self.assertEqual(results, expected_data)

    @responses.activate
    def test_get_failed_servers_with_timeout(self):
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

        responses.add(responses.GET, 'https://rosalind.info', body=ConnectionError('Not reachable'))
        responses.add(responses.GET, 'http://rosalind.info', status=200)
        responses.add(responses.GET, 'http://vika.space', status=301)
        responses.add(responses.GET, 'https://vika.space', status=302)
        results = list(get_failed_servers(servers))

        expected_data = [
            ('https://rosalind.info', 'Not reachable'),
        ]
        self.assertEqual(results, expected_data)

    @responses.activate
    def test_get_failed_servers_with_connection_error(self):
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

        responses.add(responses.GET, 'https://rosalind.info', body=ConnectionError('Not reachable'))
        responses.add(responses.GET, 'http://rosalind.info', status=200)
        responses.add(responses.GET, 'http://vika.space', body=ConnectTimeout('Timeout'))
        responses.add(responses.GET, 'https://vika.space', status=302)
        results = list(get_failed_servers(servers))

        expected_data = [
            ('https://rosalind.info', 'Not reachable'), ('http://vika.space', 'Timeout')
        ]
        self.assertEqual(sorted(results), sorted(expected_data))

    @responses.activate
    def test_get_failed_servers_with_some_expection(self):
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

        responses.add(
            responses.GET, 'https://rosalind.info', body=ValueError('Value error exception')
        )
        responses.add(responses.GET, 'http://rosalind.info', status=200)
        responses.add(responses.GET, 'http://vika.space', body=Exception('UnkownException'))
        responses.add(responses.GET, 'https://vika.space', status=302)
        results = list(get_failed_servers(servers))

        expected_data = [
            ('https://rosalind.info', 'Value error exception'),
            ('http://vika.space', 'UnkownException')
        ]
        self.assertEqual(sorted(results), sorted(expected_data))

    @responses.activate
    def test_get_failed_servers_without_failures(self):
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

        responses.add(responses.GET, 'https://rosalind.info', status=200)
        responses.add(responses.GET, 'http://rosalind.info', status=200)
        responses.add(responses.GET, 'http://vika.space', status=301)
        responses.add(responses.GET, 'https://vika.space', status=302)
        results = list(get_failed_servers(servers))

        expected_data = []
        self.assertEqual(results, expected_data)


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
