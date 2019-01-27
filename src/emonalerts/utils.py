#!/usr/bin/env python
"""
Different help functions for Easy MonAlerts
"""
import logging
logger = logging.getLogger(__name__)


def get_urls(host_settings):
    '''
    Rules:
    1. If there is no any host
        -> raise Exception
    2. If there is no any ports and schemes
        -> return HTTP://{host}
    3. If there is no any ports
        -> return [{scheme}://{host}]
    4. If there is no any schemes
        -> return [HTTP://{host}:{port}]
    5. If there is 443 port
        -> return [HTTPS://{host}]
    6. If there is 80 port
        -> return [HTTP://{host}]
    7. If there is not <http> scheme
        -> return [{scheme}://{host}] (ignore other ports)
    8. If every fields (host, schemes, ports) are filled in
        -> return [{scheme}://{host}:port]
    '''
    # Checking these rules: https://ibm.co/2Dru6sA
    # without pathes and queries

    host = host_settings.get('host')
    if not host:
        logger.exception('No any host in TOML settings')
        return []

    ports = host_settings.get('ports', [])
    schemes = host_settings.get('schemes', [])

    if not ports and not schemes:
        return f'http://{host}'

    if not ports:
        return [f'{scheme}://{host}' for scheme in schemes]

    if not schemes:
        result_urls = []
        for port in ports:
            # TODO: check other schemes <-> ports
            if port == 443:
                result_urls.append(f'https://{host}')
            elif port == 80:
                result_urls.append(f'http://{host}')
            else:
                result_urls.append(f'http://{host}:{port}')
        return result_urls

    result_urls = set()
    for scheme in schemes:
        result_urls.add(f'{scheme}://{host}')
        for port in ports:
            if port == 80:
                result_urls.add(f'http://{host}')
            if port == 443:
                result_urls.add(f'https://{host}')
            else:
                result_urls.add(f'http://{host}:{port}')
    return list(result_urls)
