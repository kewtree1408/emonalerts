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
    Uptime(
        url=url,
        successful=successful,
        unsuccessful=unsuccessful,
        amount_of_checks=amount_of_checks
    )


@db_session
def update_uptime_table(url, successful, unsuccessful, amount_of_checks):
    uptime_data = Uptime.get(url=url)
    if uptime_data is None:
        insert_uptime_table(url, successful, unsuccessful, amount_of_checks)
        return

    uptime_data.successful = successful
    uptime_data.unsuccessful = unsuccessful
    uptime_data.amount_of_checks = amount_of_checks


@db_session
def get_uptime_data(url):
    uptime_data = Uptime.get(url=url)
    if uptime_data is None:
        return (None, None, None)
    return (uptime_data.successful, uptime_data.unsuccessful, uptime_data.amount_of_checks)


@db_session
def insert_alert_table(owner_name, error_amount, alert_needed):
    Alert(owner_name=owner_name, error_amount=error_amount, alert_needed=alert_needed)


@db_session
def update_alert_table(owner_name, error_amount, alert_needed):
    alert_data = Alert.get(owner_name=owner_name)
    if alert_data is None:
        insert_alert_table(owner_name, error_amount, alert_needed)
        return

    alert_data.error_amount = error_amount
    alert_data.alert_needed = alert_needed


@db_session
def get_alert_data(owner_name):
    alert_data = Alert.get(owner_name=owner_name)
    if alert_data is None:
        return (None, None)

    return (alert_data.error_amount, alert_data.alert_needed)


def is_alert_owner_empty(owner_name):
    return get_alert_data(owner_name) is None
