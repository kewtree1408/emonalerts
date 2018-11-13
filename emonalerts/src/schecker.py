#!/usr/bin/env python
"""
Schecker: server's checker
"""

import requests
import toml
import logging
from requests.compat import urljoin
import src.funny_emos as funny_emos
from src.esender import send_from_gmail

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
            yield create_url(proto, host_settings.get("hostname"), port)


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
                yield (url, ex)


def have_to_send_alert(file_path):
    last_line = 0
    try:
        with open(file_path, 'r') as f:
            last_line = int(f.readlines()[-1])
    except FileNotFoundError as exc:
        logger.info(funny_emos.first_run(file_path))

    logger.info(f'The amount of failed servers was {last_line} before.')
    if last_line:
        return False
    return True


def save_to_error_file(file_path, amount_of_errors):
    with open(file_path, 'a+') as f:
        f.write(f'{amount_of_errors}\n')


def check(args, settings):
    amount_of_errors = 0
    problems = {}
    for url, error_msg in get_failed_servers(settings['servers']):
        amount_of_errors += 1
        logger.info(f'Something goes wrong with {url}: {error_msg}')
        problems[url] = error_msg

    if args.alert and have_to_send_alert(args.file):
        owner_settings = settings['owner']
        name = owner_settings['name']
        logger.info(f'Going to send the alert to {owner_settings["name"]}')
        send_from_gmail(args.email_credentials, owner_settings['emails'], problems)
        save_to_error_file(args.file, amount_of_errors)
