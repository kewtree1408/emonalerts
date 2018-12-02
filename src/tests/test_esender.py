#!/usr/bin/env python


import unittest
from requests.exceptions import (
    ConnectionError,
    ConnectTimeout,
    ContentDecodingError,
)
from email.message import EmailMessage
from emonalerts.esender import (
    get_email_message,
    send_from_gmail,
)


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
        # get_email_message()
        pass


class TestSendGmail(unittest.TestCase):

    def test_send_gmail_incorrect_credentials(self):
        pass

    def test_send_gmail_correct_credentials(self):
        pass

    def test_send_gmail_with_problems(self):
        pass

    def test_send_gmail_without_problems(self):
        pass

    def test_send_gmail_with_verbose(self):
        pass

    def test_send_gmail_without_verbose(self):
        pass
