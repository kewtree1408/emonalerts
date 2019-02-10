#!/usr/bin/env python
"""
Dbcmds - simple queries to sqlite3 database
"""

import logging
from emonalerts.db.models import (
    URLOwner,
    Alert,
    History,
)
from datetime import datetime
from pony.orm.core import *

logger = logging.getLogger(__name__)


@db_session
def insert_history_table(owner, url, status):
    url_owner = URLOwner.get(owner=owner, url=url)
    if not url_owner:
        url_owner = URLOwner(url=url, owner=owner)
    url_owner.history_records.create(status=status)


@db_session
def upsert_history_table(owner, url, status):
    url_owner = URLOwner.get(owner=owner, url=url)
    if not url_owner:
        url_owner = URLOwner(url=url, owner=owner)

    h = History.get(url=url_owner)
    if h:
        h.status = status
        h.timestamp = datetime.now()
    else:
        History(url=url_owner, status=status)


@db_session
def update_history_table(owner, url, status):
    url_owner = URLOwner.get(owner=owner, url=url)
    if not url_owner:
        return

    h = History.get(url=url_owner)
    if h:
        h.status = status
        h.timestamp = datetime.now()


@db_session
def update_alert_table(owner, url, is_ok):
    owner = URLOwner(url=url, owner=owner)
    owner.alerts.create(is_ok=is_ok)


@db_session
def is_url_success(owner, url):
    owner = URLOwner(url=url, owner=owner)
    if not owner.alerts:
        raise ValueError()
    return owner.alerts[0].success
