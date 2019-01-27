#!/usr/bin/env python
"""
Dbcmds - simple queries to sqlite3 database
"""

import logging
from emonalerts.db.models import (
    Alert,
    Uptime,
)
from pony.orm.core import *

logger = logging.getLogger(__name__)


@db_session
def insert_uptime_table(url, successful, unsuccessful, amount_of_checks):
    # edb = EasyORM('uptime')
    # column_value = {
    #     'url': url,
    #     'successful': successful,
    #     'unsuccessful': unsuccessful,
    #     'amount_of_checks': amount_of_checks
    # }
    # edb.insert_record(**column_value)

    Uptime(
        url=url,
        successful=successful,
        unsuccessful=unsuccessful,
        amount_of_checks=amount_of_checks
    )


@db_session
def update_uptime_table(url, successful, unsuccessful, amount_of_checks):
    # edb = EasyORM('uptime')
    # prev_succ, prev_unsucc, prev_amount = get_uptime_data(url)
    # update_data = {
    #     'set_data': {
    #         'successful': prev_succ + successful,
    #         'unsuccessful': prev_unsucc + unsuccessful,
    #         'amount_of_checks': prev_amount + amount_of_checks
    #     },
    #     'where_data': {
    #         'url': url
    #     }
    # }
    # edb.update_record(**update_data)

    uptime_data = Uptime.get(url=url)
    if uptime_data is None:
        return

    uptime_data.successful = successful
    uptime_data.unsuccessful = unsuccessful
    uptime_data.amount_of_checks = amount_of_checks


@db_session
def get_uptime_data(url):
    # edb = EasyORM('uptime')
    # get_data = {
    #     'get_data': ['successful', 'unsuccessful', 'amount_of_checks'],
    #     'where_data': {
    #         'url': url
    #     }
    # }
    # data = edb.get_data(**get_data)
    # logger.info(data)
    # return data

    uptime_data = Uptime.get(url=url)
    if uptime_data is None:
        return (None, None, None)
    return (uptime_data.successful, uptime_data.unsuccessful, uptime_data.amount_of_checks)


@db_session
def insert_alert_table(owner_name, error_amount, alert_needed):
    # edb = EasyORM('alert')
    # column_value = {
    #     'owner_name': owner_name,
    #     'error_amount': error_amount,
    #     'alert_needed': int(alert_needed)
    # }
    # edb.insert_record(**column_value)

    Alert(owner_name=owner_name, error_amount=error_amount, alert_needed=alert_needed)


@db_session
def update_alert_table(owner_name, error_amount, alert_needed):
    # edb = EasyORM('alert')
    # update_data = {
    #     'set_data': {
    #         'error_amount': error_amount,
    #         'alert_needed': int(alert_needed)
    #     },
    #     'where_data': {
    #         'owner_name': owner_name
    #     }
    # }
    # edb.update_record(**update_data)

    alert_data = Alert.get(owner_name=owner_name)
    if alert_data is None:
        return

    alert_data.error_amount = error_amount
    alert_data.alert_needed = alert_needed


@db_session
def get_alert_data(owner_name):
    # edb = EasyORM('alert')
    # get_data = {
    #     'get_data': ['error_amount', 'alert_needed'],
    #     'where_data': {
    #         'owner_name': owner_name
    #     }
    # }
    # data = edb.get_data(**get_data)
    # logger.info(data)
    # return data

    alert_data = Alert.get(owner_name=owner_name)
    if alert_data is None:
        return (None, None)

    return (alert_data.error_amount, alert_data.alert_needed)


def is_alert_owner_empty(owner_name):
    return get_alert_data(owner_name) is None