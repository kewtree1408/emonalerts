#!/usr/bin/env python
"""
Schecker: server's checker
"""

import requests
import toml
import json
import logging
from requests.compat import urljoin
import emonalerts.dbcmds as dbc
import emonalerts.funny_emos as funny_emos
from emonalerts.esender import send_via_smtp
from emonalerts.utils import get_urls

logger = logging.getLogger(__name__)


def get_settings(config_path):
    with open(config_path, 'r') as f:
        data = toml.load(f)
    return data


def get_failed_servers(servers):
    for friendly_name in servers:
        hostname = servers[friendly_name].get('host')
        if not hostname:
            continue

        for url in get_urls(servers[friendly_name]):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code >= 400:
                    yield (url, response.status_code)
            except requests.exceptions.RequestException as exc:
                # dbc.increase_uptime_table(url, percentage)
                yield (url, exc.args[0])
            except Exception as exc:
                yield (url, exc.args[0])


def have_to_send_alert(owner_name):
    last_errors, need_to_send_alert = dbc.get_alert_data(owner_name)
    logger.info(f'The amount of errors was {last_errors} before.')
    logger.info(f'need_to_send_alert = {need_to_send_alert}, {bool(int(need_to_send_alert))}.')
    found_errors = bool(last_errors != 0)
    return found_errors and bool(int(need_to_send_alert))


def get_smtp_settings(email_cred_file):
    smtp_settings = {}
    with open(email_cred_file) as f:
        data = json.loads(f.read())
        smtp_settings['email'] = data['email']
        smtp_settings['password'] = data['password']
        smtp_settings['host'] = data.get('host', 'smtp.gmail.com')
        smtp_settings['port'] = int(data.get('port', 465))
    return smtp_settings


def check(args, settings):
    owner_settings = settings['owner']
    owner_name = owner_settings['name']
    amount_of_errors = 0
    problems = {}
    for url, error_msg in get_failed_servers(settings['servers']):
        amount_of_errors += 1
        if have_to_send_alert(owner_name):
            dbc.update_alert_table(owner_name, amount_of_errors, False)
        logger.info(f'Something goes wrong with {url}: {error_msg}')
        problems[url] = error_msg

    if args.alert and have_to_send_alert(owner_name):
        name = owner_settings['name']
        logger.info(f'Going to send the alert to {owner_settings["name"]}')
        smtp_settings = get_smtp_settings(args.email_credentials)
        send_via_smtp(smtp_settings, owner_settings['emails'], problems)

    if amount_of_errors == 0:
        dbc.update_alert_table(owner_name, amount_of_errors, True)
