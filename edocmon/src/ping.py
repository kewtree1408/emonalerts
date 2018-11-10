#!/usr/bin/env python

import argparse
import requests
import toml
import ipdb
import logging
import requests
from requests.compat import urljoin

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


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


def failed_servers(servers):
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


def send_alert(to_owner, url, error):
    pass


def main():
    parser = argparse.ArgumentParser(description='Set up settings for monitoring')
    parser.add_argument('config', type=str, help='path to toml-config file')
    parser.add_argument('-a', '--alert', action='store_true', help='ignore alerts')
    args = parser.parse_args()

    settings = get_settings(args.config)
    logging.info(f'Get settings: {settings}')
    for url, error_msg in failed_servers(settings['servers']):
        logging.info(f'Something goes wrong with {url}: {error_msg}')
        if args.alert:
            to_owner = settings['owner']
            logging.info(f'Going to send the alert to {to_owner["name"]}')
            send_alert(to_owner, url, error_msg)


if __name__ == "__main__":
    main()