#!/usr/bin/env python
"""
Runner: entrypoint of the EasyMonAlerts app
"""

import argparse
import logging
import time
import sys

from schecker import (
    check,
    get_settings,
)

def setup_logger():
    root = logging.getLogger()
    root.setLevel(logging.WARNING)
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


def main():
    logger = setup_logger()

    parser = argparse.ArgumentParser(description='Set up settings for monitoring')
    parser.add_argument('config', type=str, help='path to toml-config file')
    parser.add_argument('email_credentials', type=str, help='path to email credentails.json')
    parser.add_argument('-a', '--alert', action='store_true', help='ignore alerts')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose mode')
    parser.add_argument('-f', '--file', default='alerts.err', help='file with amount of errors')
    args = parser.parse_args()

    if args.verbose:
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

    settings = get_settings(args.config)
    logging.info(f'Get settings: {settings}')
    while True:
        try:
            minutes = int(settings['period']['minutes']*60)
            check(args, settings)
            time.sleep(minutes)
        except KeyboardInterrupt as exc:
            logger.info('EasyMonAlerts was ended by user.')
            return 0


if __name__ == "__main__":
    main()