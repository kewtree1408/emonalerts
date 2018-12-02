#!/usr/bin/env python
"""
Dbcmds - simple queries to sqlite3 database
"""

import logging
from emonalerts.easyorm import EasyORM

logger = logging.getLogger(__name__)


def create_uptime_table():
    edb = EasyORM('uptime')
    column_type = {
        'url': 'text',
        'successful': 'integer',
        'unsuccessful': 'integer',
        'amount_of_checks': 'integer'
    }
    edb.create_table(**column_type)


def insert_uptime_table(url, successful, unsuccessful, amount_of_checks):
    edb = EasyORM('uptime')
    column_value = {
        'url': url,
        'successful': successful,
        'unsuccessful': unsuccessful,
        'amount_of_checks': amount_of_checks
    }
    edb.insert_record(**column_value)


def update_uptime_table(url, successful, unsuccessful, amount_of_checks):
    edb = EasyORM('uptime')
    prev_succ, prev_unsucc, prev_amount = get_uptime_data(url)
    update_data = {
        'set_data': {
            'successful': prev_succ + successful,
            'unsuccessful': prev_unsucc + unsuccessful,
            'amount_of_checks': prev_amount + amount_of_checks
        },
        'where_data': {
            'url': url
        }
    }
    edb.update_record(**update_data)


def get_uptime_data(url):
    edb = EasyORM('uptime')
    get_data = {
        'get_data': ['successful', 'unsuccessful', 'amount_of_checks'],
        'where_data': {
            'url': url
        }
    }
    data = edb.get_data(**get_data)
    logger.info(data)
    return data


def create_alert_table():
    edb = EasyORM('alert')
    column_type = {
        'owner_name': 'text',
        'error_amount': 'integer',
        'alert_needed': 'boolean'
    }
    edb.create_table(**column_type)


def insert_alert_table(owner_name, error_amount, alert_needed):
    edb = EasyORM('alert')
    column_value = {
        'owner_name': owner_name,
        'error_amount': error_amount,
        'alert_needed': int(alert_needed)
    }
    edb.insert_record(**column_value)


def update_alert_table(owner_name, error_amount, alert_needed):
    edb = EasyORM('alert')
    update_data = {
        'set_data': {
            'error_amount': error_amount,
            'alert_needed': int(alert_needed)
        },
        'where_data': {
            'owner_name': owner_name
        }
    }
    edb.update_record(**update_data)


def get_alert_data(owner_name):
    edb = EasyORM('alert')
    get_data = {
        'get_data': ['error_amount', 'alert_needed'],
        'where_data': {
            'owner_name': owner_name
        }
    }
    data = edb.get_data(**get_data)
    logger.info(data)
    return data


def is_alert_owner_empty(owner_name):
    return get_alert_data(owner_name) is None