#!/usr/bin/env python

import unittest
from emonalerts.utils import get_urls


class TestHostSettings(unittest.TestCase):
    def test_filled_in_settings(self):
        host_settings = {
            'host': 'google.com',
            'schemes': ['udp', 'http', 'https'],
            'ports': [443, 8080, 1234]
        }
        expected_urls = [
            'http://google.com:1234', 'http://google.com:8080', 'https://google.com',
            'https://google.com', 'udp://google.com'
        ]
        result_urls = sorted(get_urls(host_settings))
        self.assertEqual(result_urls, sorted(expected_urls))

    def test_missing_host_settings(self):
        host_settings = {'schemes': ['udp', 'http'], 'ports': [443, 8080, 1234]}
        expected_urls = []
        result_urls = get_urls(host_settings)
        self.assertEqual(result_urls, sorted(expected_urls))

    def test_missing_schemes_settings(self):
        host_settings = {'host': 'yandex.com', 'ports': [443, 8080, 1234, 5555, 80]}
        expected_urls = [
            'http://yandex.com:1234',
            'http://yandex.com:8080',
            'http://yandex.com:5555',
            'http://yandex.com',
            'https://yandex.com',
        ]
        result_urls = sorted(get_urls(host_settings))
        self.assertEqual(result_urls, sorted(expected_urls))

    def test_missing_ports_settings(self):
        host_settings = {'schemes': ['ftp', 'http', 'https'], 'host': 'facebook.com'}
        expected_urls = ['https://facebook.com', 'ftp://facebook.com', 'http://facebook.com']
        result_urls = sorted(get_urls(host_settings))
        self.assertEqual(result_urls, sorted(expected_urls))

    def test_empty_host_settings(self):
        host_settings = {}
        expected_urls = []
        result_urls = sorted(get_urls(host_settings))
        self.assertEqual(result_urls, sorted(expected_urls))

    def test_additional_host_settings(self):
        host_settings = {
            'host': 'apple.com',
            'schemes': ['udp', 'http', 'https'],
            'ports': [443, 8080, 1234],
            'ips': ['198.120.0.1', '0.0.0.0']
        }
        expected_urls = [
            'http://apple.com:1234', 'http://apple.com:8080', 'https://apple.com',
            'https://apple.com', 'udp://apple.com'
        ]
        result_urls = sorted(get_urls(host_settings))
        self.assertEqual(result_urls, sorted(expected_urls))
