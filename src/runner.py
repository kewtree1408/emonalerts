#!/usr/bin/env python
"""
Runner: entrypoint of the EasyMonAlerts app
"""

import argparse
import logging
import time
import sys

import emonalerts.db.cmds as dbc

from emonalerts.schecker import (
    check,
    get_settings,
)

def setup_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    format_schema = '[%(levelname)s] [%(filename)s/%(funcName)s]:\n%(asctime)s:%(message)s'
    formatter = logging.Formatter(format_schema)
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    root.addHandler(ch)
    root.addHandler(fh)
    return root


def infinitive_check(args):

    logger = setup_logger()
    settings = get_settings(args.config)
    owner_name = settings['owner']['name']
    if dbc.is_alert_owner_empty(owner_name):
        dbc.insert_alert_table(owner_name, 0, False)

    logger.info(f'Get settings: {settings}')
    while True:
        try:
            minutes = int(settings['period']['minutes']*60)
            check(args)
            time.sleep(minutes)
        except KeyboardInterrupt as exc:
            logger.info('EasyMonAlerts was ended by user.')
            return
        except Exception as exc:
            logger.exception(f'Unknown error: {exc}')
            return


def parse_args():
    parser = argparse.ArgumentParser(description='Set up settings for alerts and monitoring')
    parser.add_argument('config', type=str, help='path to toml-config file')
    parser.add_argument(
        '-e',
        '--email',
        required=False,
        dest='email_credentials',
        type=str,
        help='path to email credentails.json'
    )
    parser.add_argument('-a', '--alert', action='store_true', help='ignore alerts')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    return parser


def main():
    logger = setup_logger()
    parser = parse_args()
    args = parser.parse_args()

    if args.verbose:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    infinitive_check(args)


if __name__ == "__main__":
    main()
