#!/usr/bin/env python

import unittest
from unittest.mock import patch
from pathlib import Path

from runner import (
    infinitive_check,
    parse_args,
)

class TestRunner(unittest.TestCase):

    def setUp(self):
        self.parser = parse_args()
        self.cur_dir = Path.cwd()
        self.setting_path = str(self.cur_dir.joinpath('src/tests/inputs/settings.toml'))
        self.credential_path = str(self.cur_dir.joinpath('src/tests/inputs/creds.json'))

    def test_parsing_args(self):
        args = self.parser.parse_args(['test', 'test2', '-a', '-v'])
        self.assertEqual(args.config, 'test')
        self.assertEqual(args.email_credentials, 'test2')
        self.assertEqual(args.alert, True)
        self.assertEqual(args.verbose, True)

    @patch('runner.check')
    def test_keyboard_interrupt_exception(self, mock_check):
        args = self.parser.parse_args([
            self.setting_path,
            self.credential_path,
            '-a',
            '-v'
        ])
        mock_check.side_effect = KeyboardInterrupt('Stop!')
        infinitive_check(args)
        assert mock_check.called

    @patch('runner.check')
    def test_any_other_exception(self, mock_check):
        args = self.parser.parse_args([
            self.setting_path,
            self.credential_path,
            '-a',
            '-v'
        ])
        mock_check.side_effect = Exception('Boom!')
        infinitive_check(args)
        assert mock_check.called
