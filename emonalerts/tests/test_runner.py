#!/usr/bin/env python

import unittest
from unittest.mock import patch

from src.runner import (
    infinitive_check,
    parse_args,
)

class TestRunner(unittest.TestCase):

    def setUp(self):
        self.parser = parse_args()

    def test_parsing_args(self):
        args = self.parser.parse_args(['test', 'test2', '-a', '-v', '-f', 'aleeert.err'])
        self.assertEqual(args.config, 'test')
        self.assertEqual(args.email_credentials, 'test2')
        self.assertEqual(args.alert, True)
        self.assertEqual(args.verbose, True)
        self.assertEqual(args.file, 'aleeert.err')

    @patch('src.runner.check')
    def test_keyboard_interrupt_exception(self, mock_check):
        args = self.parser.parse_args(['tests/inputs/settings.toml', 'tests/inputs/creds.json', '-a', '-v', '-f', 'aleeert.err'])
        mock_check.side_effect = KeyboardInterrupt('Stop!')
        infinitive_check(args)
        assert mock_check.called

    @patch('src.runner.check')
    def test_any_other_exception(self, mock_check):
        args = self.parser.parse_args(['tests/inputs/settings.toml', 'tests/inputs/creds.json', '-a', '-v', '-f', 'aleeert.err'])
        mock_check.side_effect = Exception('Boom!')
        infinitive_check(args)
        assert mock_check.called
