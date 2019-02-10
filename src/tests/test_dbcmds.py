#!/usr/bin/env python

import unittest
from datetime import datetime
import emonalerts.db.cmds as dbcmd
from emonalerts.db.models import (
    Alert,
    History,
    URLOwner,
)
from pony.orm.core import *


class TestHistoryDBCommands(unittest.TestCase):
    @db_session
    def setUp(self):
        self.url = 'https://yandex.com'
        self.owner = 'me'
        URLOwner.select().delete(bulk=True)

    @db_session
    def test_insert_exists_record(self):
        now = datetime.now()
        dbcmd.insert_history_table(self.owner, self.url, 'OK')
        dbcmd.insert_history_table(self.owner, self.url, 'notOK')
        url_owner = URLOwner.get(owner=self.owner, url=self.url)
        history_records = History.select()[:]
        last_h = history_records[-1]
        self.assertEqual(len(history_records), 2)
        self.assertEqual(last_h.status, 'notOK')
        self.assertGreater(last_h.timestamp, now)

    @db_session
    def test_upsert_exists_record(self):
        now = datetime.now()
        dbcmd.upsert_history_table(self.owner, self.url, 'OK')
        dbcmd.upsert_history_table(self.owner, self.url, 'notOK')
        url_owner = URLOwner.get(owner=self.owner, url=self.url)
        history_records = History.select()[:]
        last_h = history_records[-1]
        self.assertEqual(len(history_records), 1)
        self.assertEqual(last_h.status, 'notOK')
        self.assertGreater(last_h.timestamp, now)

    @db_session
    def test_update_exists_record(self):
        now = datetime.now()
        dbcmd.insert_history_table(self.owner, self.url, 'OK')
        dbcmd.update_history_table(self.owner, self.url, 'notOK')
        url_owner = URLOwner.get(owner=self.owner, url=self.url)
        history_records = History.select()[:]
        last_h = history_records[-1]
        self.assertEqual(len(history_records), 1)
        self.assertEqual(last_h.status, 'notOK')
        self.assertGreater(last_h.timestamp, now)

    @db_session
    def test_update_not_existed_record(self):
        now = datetime.now()
        dbcmd.update_history_table(self.owner, self.url, 'OK')
        dbcmd.update_history_table(self.owner, self.url, 'notOK')
        url_owner = URLOwner.get(owner=self.owner, url=self.url)
        history_records = History.select()[:]
        self.assertEqual(len(history_records), 0)


#     @db_session
#     def test_get_exists_record(self):
#         dbcmd.insert_uptime_table(self.url, 10, 11, 21)
#         uptime_results = dbcmd.get_uptime_data(self.url)
#         expected_results = (10, 11, 21)
#         self.assertEqual(uptime_results, expected_results)

#     @db_session
#     def test_get_empty_record(self):
#         u = dbcmd.get_uptime_data(self.url)
#         expected_results = (None, None, None)
#         self.assertEqual(u, expected_results)

# class TestAlertDBCommands(unittest.TestCase):
#     @db_session
#     def setUp(self):
#         self.owner_name = u'Виктория Fantasy'
#         Alert.select().delete(bulk=True)

#     @db_session
#     def test_insert(self):
#         dbcmd.insert_alert_table(self.owner_name, 10, True)
#         a = Alert.get(owner_name=self.owner_name)
#         alert_results = (a.owner_name, a.error_amount, a.alert_needed)
#         expected_results = (self.owner_name, 10, True)
#         self.assertEqual(alert_results, expected_results)

#     @db_session
#     def test_update_exists_record(self):
#         dbcmd.insert_alert_table(self.owner_name, 15, False)
#         dbcmd.update_alert_table(self.owner_name, 10, True)
#         a = Alert.get(owner_name=self.owner_name)
#         alert_results = (a.owner_name, a.error_amount, a.alert_needed)
#         expected_results = (self.owner_name, 10, True)
#         self.assertEqual(alert_results, expected_results)

#     @db_session
#     def test_update_empty_record(self):
#         dbcmd.update_alert_table(self.owner_name, 20, True)
#         a = Alert.get(owner_name=self.owner_name)
#         self.assertNotEqual(a, None)

#     @db_session
#     def test_get_exists_record(self):
#         dbcmd.insert_alert_table(self.owner_name, 25, False)
#         alert_results = dbcmd.get_alert_data(self.owner_name)
#         expected_results = (25, False)
#         self.assertEqual(alert_results, expected_results)

#     @db_session
#     def test_get_empty_record(self):
#         a = dbcmd.get_alert_data(self.owner_name)
#         expected_results = (None, None)
#         self.assertEqual(a, expected_results)
