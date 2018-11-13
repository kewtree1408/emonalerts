#!/usr/bin/env python
"""
Esender - email sender
"""

import json
import logging
from smtplib import SMTP_SSL
from email.message import EmailMessage
import src.funny_emos as funny_emos


logger = logging.getLogger(__name__)


def get_email_message(sender, recipient, problems):
    msg = EmailMessage()
    msg['Subject'] = funny_emos.get_msg_subject()
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content(funny_emos.get_msg_content(problems))
    return msg


def send_from_gmail(email_cred, to_emails, problems, verbose=False):
    """
    Send email via passed credentials
    """
    smtp_settings = {}
    with open(email_cred) as f:
        data = json.loads(f.read())
        smtp_settings['email'] = data['email']
        smtp_settings['password'] = data['password']
        smtp_settings['host'] = data.get('host', 'smtp.gmail.com')
        smtp_settings['port'] = int(data.get('port', 465))

    with SMTP_SSL(host=smtp_settings['host'], port=smtp_settings['port']) as smtp_server:
        smtp_server.login(data['email'], data['password'])
        if verbose:
            logger.info(f"EasyMon Alerts logged into {smtp_settings['host']} successfully!")
            smtp_server.set_debuglevel(1)

        for to_email in to_emails:
            msg = get_email_message(data['email'], to_email, problems)
            logger.info(f'EasyMon Alerts is going to send the email with details to {to_email}...')
            smtp_server.send_message(msg)
