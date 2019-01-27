#!/usr/bin/env python

import unittest
from unittest.mock import (
    patch,
    Mock,
)
from emonalerts.db.models import (
    Alert,
    Uptime,
)
from pony.orm.core import *

import responses
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
)

from emonalerts.schecker import (
    get_failed_servers,
    have_to_send_alert,
    check,
)
import emonalerts.db.cmds as dbc


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
    def test_with_data_in_db(self):
        last_errors, need_to_send_alert = 5, True
        current_errors = 0
        with patch(
                'emonalerts.schecker.dbc.get_alert_data',
                return_value=(last_errors, need_to_send_alert),
        ) as mock_method:
            result = have_to_send_alert('me', 0)
        self.assertEqual(result, True)

    def test_with_last_errors(self):
        last_errors, need_to_send_alert = 5, False
        current_errors = 5
        with patch(
                'emonalerts.schecker.dbc.get_alert_data',
                return_value=(last_errors, need_to_send_alert),
        ) as mock_method:
            result = have_to_send_alert('me', current_errors)
        self.assertEqual(result, False)

    def test_without_data_in_db(self):
        last_errors, need_to_send_alert = None, None
        current_errors = 0
        with patch(
                'emonalerts.schecker.dbc.get_alert_data',
                return_value=(last_errors, need_to_send_alert),
        ) as mock_method:
            result = have_to_send_alert('me', current_errors)
        self.assertEqual(result, True)


class TestCheck(unittest.TestCase):
    @db_session
    def setUp(self):
        Alert.select().delete(bulk=True)

    @responses.activate
    def test_check_successful(self):
        owner_name = 'Victoria'
        settings = {
            'owner': {
                'name': owner_name,
                'emails': [
                    'vi@umc8.ru',
                    'me@vika.space',
                ]
            },
            'servers': {
                'server1': {
                    'host': 'google.com',
                    'schemes': ['http', 'https'],
                    'ports': [8080, 9090],
                },
                'server2': {
                    'host': 'yandex.com',
                    'schemes': ['https'],
                },
            }
        }
        mock_args = Mock()
        mock_args.alert = True

        responses.add(responses.GET, 'https://google.com', status=200)
        responses.add(responses.GET, 'http://google.com', status=202)
        responses.add(responses.GET, 'http://google.com:8080', status=302)
        responses.add(responses.GET, 'http://google.com:9090', status=301)
        responses.add(responses.GET, 'https://yandex.com', status=200)

        email_credentials = {
            'email': 'mon.alerts@gmail.com',
            'password': 'testme',
            'host': 'smtp.gmail.com',
            'port': 465,
        }
        with patch('emonalerts.schecker.send_via_smtp', return_value=None) as p2, \
             patch('emonalerts.schecker.get_smtp_settings', return_value=email_credentials) as p1:
            check(mock_args, settings)

        amount_of_errors, will_send_emails = dbc.get_alert_data(owner_name)
        self.assertEqual(amount_of_errors, 0)
        # True -> because it's first run
        self.assertEqual(will_send_emails, True)

    @responses.activate
    def test_check_unsuccessful(self):
        owner_name = 'Victoria'
        settings = {
            'owner': {
                'name': owner_name,
                'emails': [
                    'vi@umc8.ru',
                    'me@vika.space',
                ]
            },
            'servers': {
                'server1': {
                    'host': 'google.com',
                    'schemes': ['http', 'https'],
                    'ports': [8080, 9090],
                },
                'server2': {
                    'host': 'yandex.com',
                    'schemes': ['https'],
                },
            }
        }
        mock_args = Mock()
        mock_args.alert = True

        responses.add(responses.GET, 'https://google.com', status=404)
        responses.add(responses.GET, 'http://google.com', status=500)
        responses.add(responses.GET, 'http://google.com:8080', status=400)
        responses.add(responses.GET, 'http://google.com:9090', status=301)
        responses.add(responses.GET, 'https://yandex.com', status=200)

        email_credentials = {
            'email': 'mon.alerts@gmail.com',
            'password': 'testme',
            'host': 'smtp.gmail.com',
            'port': 465,
        }
        with patch('emonalerts.schecker.send_via_smtp', return_value=None) as p2, \
             patch('emonalerts.schecker.get_smtp_settings', return_value=email_credentials) as p1:
            check(mock_args, settings)

        amount_of_errors, will_send_emails = dbc.get_alert_data(owner_name)
        self.assertEqual(amount_of_errors, 3)
        # True -> because it's first run
        self.assertEqual(will_send_emails, True)

        with patch('emonalerts.schecker.send_via_smtp', return_value=None) as p2, \
             patch('emonalerts.schecker.get_smtp_settings', return_value=email_credentials) as p1:
            check(mock_args, settings)

        amount_of_errors, will_send_emails = dbc.get_alert_data(owner_name)
        self.assertEqual(amount_of_errors, 3)
        # True -> because it's first run
        self.assertEqual(will_send_emails, False)
