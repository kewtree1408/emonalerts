#!/usr/bin/env python
"""
Models for Emonalerts
"""

import emonalerts.settings as settings
from pony.orm.core import *

db = Database("sqlite", settings.DB_NAME, create_db=True)


# Uptime table - not using right not
class Uptime(db.Entity):
    url = Required(unicode, unique=True)
    successful = Required(int)
    unsuccessful = Required(int)
    amount_of_checks = Required(int)


class Alert(db.Entity):
    owner_name = Required(unicode, unique=True)
    error_amount = Required(int)
    # alert_needed - not using right now
    alert_needed = Required(bool)


set_sql_debug(True)
db.generate_mapping(create_tables=True)
