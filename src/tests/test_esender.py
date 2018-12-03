#!/usr/bin/env python


import unittest
from unittest.mock import (
    patch,
    Mock,
)
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    ContentDecodingError,
)
from email.message import EmailMessage
from emonalerts.esender import (
    get_email_message,
    send_via_smtp,
)
import smtplib


class TestGetMessage(unittest.TestCase):

    def test_get_message_with_problems(self):
        problems = {
            'http://ya.ru': ConnectionError("I'm connection error"),
            'http://google.com': ConnectTimeout("I'm connection timeout error"),
            'http://duckduckgo.com': ContentDecodingError("I'm connection decoding error"),
        }
        msg = get_email_message('mon.alert@gmail.com', 'vi@umc8.ru', problems)
        self.assertEqual(type(msg), EmailMessage)
        dict_msg = dict(msg)
        self.assertEqual(dict_msg['Subject'], "You've recieved the alert from EasyMonAlerts 🕖")
        self.assertEqual(dict_msg['From'], 'mon.alert@gmail.com')
        self.assertEqual(dict_msg['To'], 'vi@umc8.ru')
        self.assertEqual(dict_msg['Content-Type'], 'text/plain; charset="utf-8"')
        self.assertEqual(dict_msg['Content-Transfer-Encoding'], 'quoted-printable')
        self.assertEqual(dict_msg['MIME-Version'], '1.0')
        self.assertEqual(msg.get_content(), "😒 Unfortinatully we have noticed some problems.\n\tURL: http://ya.ru\n\tThe error: I'm connection error\n\n\tURL: http://google.com\n\tThe error: I'm connection timeout error\n\n\tURL: http://duckduckgo.com\n\tThe error: I'm connection decoding error\n\nWe hope this message will help you to understand the problem better. Good luck! 😉\n")

    def test_get_message_without_problems(self):
        problems = {}
        msg = get_email_message('mon.alert@gmail.com', 'vi@umc8.ru', problems)
        self.assertEqual(type(msg), EmailMessage)
        dict_msg = dict(msg)
        self.assertEqual(dict_msg['Subject'], "You've recieved the alert from EasyMonAlerts 🕖")
        self.assertEqual(dict_msg['From'], 'mon.alert@gmail.com')
        self.assertEqual(dict_msg['To'], 'vi@umc8.ru')
        self.assertEqual(dict_msg['Content-Type'], 'text/plain; charset="utf-8"')
        self.assertEqual(dict_msg['Content-Transfer-Encoding'], '8bit')
        self.assertEqual(dict_msg['MIME-Version'], '1.0')
        self.assertEqual(msg.get_content(), "It looks like all your services are working perfect! 😊\n")


class TestSendViaSMTP(unittest.TestCase):
    def test_send_via_smtp_incorrect_smtp_host(self):
        smtp_settings = {
            'host': 'gmail.bla.bla',
            'port': 123,
            'email': 'from@vika.space',
            'password': '1234'
        }
        to_emails = ['to@vika.space', 'lala@vika.space', '2121@vi.space']
        problems = {}
        with patch.object(
                smtplib.SMTP_SSL,
                'connect',
                return_value=(123, 'side effect: SMTPConnectError')
            ) as mock_smtp_obj, \
            patch.object(
                smtplib.SMTP_SSL,
                'close',
                return_value=None
            ) as mock_smtp_obj_close:
                mock_smtp_obj = Mock()
                mock_smtp_obj.side_effect = smtplib.SMTPConnectError(123, 'side effect: SMTPConnectError')
                with self.assertRaises(smtplib.SMTPConnectError):
                    send_via_smtp(smtp_settings, to_emails, problems)

    def test_send_via_smtp_incorrect_credentials(self):
        smtp_settings = {
            'host': 'gmail.bla.bla',
            'port': 123,
            'email': 'from@vika.space',
            'password': '1234'
        }
        to_emails = ['to@vika.space', 'lala@vika.space', '2121@vi.space']
        problems = {}
        with patch.object(smtplib.SMTP_SSL, 'connect', return_value=(220, 'msg')) as mock_connect, \
             patch.object(smtplib.SMTP_SSL, 'close', return_value=None) as mock_close:
            with patch.object(smtplib.SMTP_SSL, 'login') as mock_login:
                mock_login.side_effect = smtplib.SMTPAuthenticationError(123, 'side effect: SMTPAuthenticationError')
                with self.assertRaises(smtplib.SMTPAuthenticationError):
                    send_via_smtp(smtp_settings, to_emails, problems)

    def test_send_via_smtp_correct_credentials(self):
        smtp_settings = {
            'host': 'gmail.bla.bla',
            'port': 123,
            'email': 'from@vika.space',
            'password': '1234'
        }
        to_emails = ['to@vika.space', 'lala@vika.space', '2121@vi.space']
        problems = {
            'http://ya.ru': ConnectionError("I'm connection error"),
            'http://google.com': ConnectTimeout("I'm connection timeout error"),
            'http://duckduckgo.com': ContentDecodingError("I'm connection decoding error"),
        }
        with patch.object(smtplib.SMTP_SSL, 'connect', return_value=(220, 'msg')) as mock_connect, \
             patch.object(smtplib.SMTP_SSL, 'close', return_value=None) as mock_close, \
             patch.object(smtplib.SMTP_SSL, 'login', return_value=None) as mock_login, \
             patch.object(smtplib.SMTP_SSL, 'send_message', return_value=None) as mock_send_msg:
                send_via_smtp(smtp_settings, to_emails, problems)
                self.assertEqual(mock_send_msg.call_count, len(to_emails))

    def test_send_via_smtp_without_problems(self):
        smtp_settings = {
            'host': 'gmail.bla.bla',
            'port': 123,
            'email': 'from@vika.space',
            'password': '1234'
        }
        to_emails = ['to@vika.space', 'lala@vika.space', '2121@vi.space']
        problems = {}
        with patch.object(smtplib.SMTP_SSL, 'connect', return_value=(220, 'msg')) as mock_connect, \
             patch.object(smtplib.SMTP_SSL, 'close', return_value=None) as mock_close, \
             patch.object(smtplib.SMTP_SSL, 'login', return_value=None) as mock_login, \
             patch.object(smtplib.SMTP_SSL, 'send_message', return_value=None) as mock_send_msg:
                send_via_smtp(smtp_settings, to_emails, problems)
                self.assertEqual(mock_send_msg.call_count, len(to_emails))
