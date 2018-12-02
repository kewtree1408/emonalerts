#!/usr/bin/env python
"""
Schecker: server's checker
"""

import requests
import toml
import logging
from requests.compat import urljoin
import emonalerts.dbcmds as dbc
import emonalerts.funny_emos as funny_emos
from emonalerts.esender import send_from_gmail

logger = logging.getLogger(__name__)


def get_settings(config_path):
    with open(config_path, 'r') as f:
        data = toml.load(f)
    return data


def create_url(proto, hostname, port):
    return f'{proto}://{hostname}:{port}'


def gen_urls(host_settings):
    for proto in host_settings.get('protocols', []):
        for port in host_settings.get('ports', []):
            yield create_url(proto, host_settings.get('hostname'), port)


def get_failed_servers(servers):
    for friendly_name in servers:
        hostname = servers[friendly_name].get('hostname')
        if not hostname:
            continue

        for url in gen_urls(servers[friendly_name]):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code >= 400:
                    yield (url, response.status_code)
            except requests.exceptions.ConnectionError as ex:
                # dbc.increase_uptime_table(url, percentage)
                yield (url, ex)


def have_to_send_alert(owner_name):
    last_errors, need_to_send_alert = dbc.get_alert_data(owner_name)
    logger.info(f'The amount of errors was {last_errors} before.')
    logger.info(f'need_to_send_alert = {need_to_send_alert}, {bool(int(need_to_send_alert))}.')
    found_errors = bool(last_errors!=0)
    return found_errors and bool(int(need_to_send_alert))


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
        send_from_gmail(args.email_credentials, owner_settings['emails'], problems)

    if amount_of_errors == 0:
        dbc.update_alert_table(owner_name, amount_of_errors, True)
