#!/usr/bin/env python
"""
Models for Emonalerts
"""

from datetime import datetime
import emonalerts.settings as settings
from pony.orm.core import *

db = Database("sqlite", settings.DB_NAME, create_db=True)


class URLOwner(db.Entity):
    owner = Required(unicode)
    url = Required(unicode)
    PrimaryKey(owner, url)

    history_records = Set('History')
    alerts = Set('Alert')


class History(db.Entity):
    url = Required(URLOwner)
    timestamp = Required(datetime, default=datetime.now)
    status = Required(str)


class Alert(db.Entity):
    url = Required(URLOwner, unique=True)
    success = Required(bool)


set_sql_debug(True)
db.generate_mapping(create_tables=True)
