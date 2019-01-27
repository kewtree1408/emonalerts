#!/usr/bin/env python

import unittest
from emonalerts.db.cmds import *
from pony.orm.core import *


class TestUptimeDBCommands(unittest.TestCase):
    @db_session
    def setUp(self):
        self.url = 'https://yandex.com'
        Uptime.select().delete(bulk=True)

    @db_session
    def test_insert(self):
        insert_uptime_table(self.url, 10, 12, 123)
        u = Uptime.get(url=self.url)
        uptime_results = (u.url, u.successful, u.unsuccessful, u.amount_of_checks)
        expected_results = (self.url, 10, 12, 123)
        self.assertEqual(uptime_results, expected_results)

    @db_session
    def test_update_exists_record(self):
        insert_uptime_table(self.url, 1, 1, 2)
        update_uptime_table(self.url, 10, 10, 20)
        u = Uptime.get(url=self.url)
        uptime_results = (u.url, u.successful, u.unsuccessful, u.amount_of_checks)
        expected_results = (self.url, 10, 10, 20)
        self.assertEqual(uptime_results, expected_results)

    @db_session
    def test_update_empty_record(self):
        update_uptime_table(self.url, 1, 1, 2)
        u = Uptime.get(url=self.url)
        self.assertEqual(u, None)

    @db_session
    def test_get_exists_record(self):
        insert_uptime_table(self.url, 10, 11, 21)
        uptime_results = get_uptime_data(self.url)
        expected_results = (10, 11, 21)
        self.assertEqual(uptime_results, expected_results)

    @db_session
    def test_get_empty_record(self):
        u = get_uptime_data(self.url)
        expected_results = (None, None, None)
        self.assertEqual(u, expected_results)


class TestAlertDBCommands(unittest.TestCase):
    @db_session
    def setUp(self):
        self.owner_name = u'Виктория Fantasy'
        Alert.select().delete(bulk=True)

    @db_session
    def test_insert(self):
        insert_alert_table(self.owner_name, 10, True)
        a = Alert.get(owner_name=self.owner_name)
        alert_results = (a.owner_name, a.error_amount, a.alert_needed)
        expected_results = (self.owner_name, 10, True)
        self.assertEqual(alert_results, expected_results)

    @db_session
    def test_update_exists_record(self):
        insert_alert_table(self.owner_name, 15, False)
        update_alert_table(self.owner_name, 10, True)
        a = Alert.get(owner_name=self.owner_name)
        alert_results = (a.owner_name, a.error_amount, a.alert_needed)
        expected_results = (self.owner_name, 10, True)
        self.assertEqual(alert_results, expected_results)

    @db_session
    def test_update_empty_record(self):
        update_alert_table(self.owner_name, 20, True)
        a = Alert.get(owner_name=self.owner_name)
        self.assertEqual(a, None)

    @db_session
    def test_get_exists_record(self):
        insert_alert_table(self.owner_name, 25, False)
        alert_results = get_alert_data(self.owner_name)
        expected_results = (25, False)
        self.assertEqual(alert_results, expected_results)

    @db_session
    def test_get_empty_record(self):
        a = get_alert_data(self.owner_name)
        expected_results = (None, None)
        self.assertEqual(a, expected_results)