#!/usr/bin/env python
"""
Esender - email sender
"""

import json
import logging
from smtplib import SMTP_SSL
from email.message import EmailMessage
import emonalerts.funny_emos as funny_emos


logger = logging.getLogger(__name__)


def get_email_message(sender, recipient, problems):
    msg = EmailMessage()
    msg['Subject'] = funny_emos.get_msg_subject()
    msg['From'] = sender
    msg['To'] = recipient
    if problems:
        msg.set_content(funny_emos.get_msg_content(problems))
    else:
        msg.set_content(funny_emos.get_msg_content_without_problems())
    return msg


def send_via_smtp(smtp_settings, to_emails, problems, verbose=False):
    """
    Send email via passed credentials

    """
    with SMTP_SSL(host=smtp_settings['host'], port=smtp_settings['port']) as smtp_server:
        smtp_server.login(smtp_settings['email'], smtp_settings['password'])
        if verbose:
            logger.info(f"EasyMon Alerts logged into {smtp_settings['host']} successfully!")
            smtp_server.set_debuglevel(1)

        for to_email in to_emails:
            msg = get_email_message(smtp_settings['email'], to_email, problems)
            logger.info(f'EasyMon Alerts is going to send the email with details to {to_email}...')
            smtp_server.send_message(msg)
