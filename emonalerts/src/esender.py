#!/usr/bin/env python
"""
Esender - email sender
"""

import json
import logging
import funny_emos
from smtplib import SMTP_SSL
from email.message import EmailMessage


def get_email_message(sender, recipient, problems):
    msg = EmailMessage()
    msg['Subject'] = funny_emos.get_msg_subject()
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content(funny_emos.get_msg_content(problems))
    return msg


def send_from_gmail(to_emails, problems, verbose=False):
    """
    Send email via gmail
    """
    smtp_settings = {
        'host': 'smtp.gmail.com',
        'port': 465
    }
    with open('./credentials.json') as f:
        data = json.loads(f.read())
        smtp_settings['email'] = data['email']
        smtp_settings['password'] = data['password']

    with SMTP_SSL(host=smtp_settings['host'], port=smtp_settings['port']) as smtp_server:
        smtp_server.login(data['email'], data['password'])
        if verbose:
            logging.info("EasyMon Alerts logged in successfully!")
            smtp_server.set_debuglevel(1)

        for to_email in to_emails:
            msg = get_email_message(data['email'], to_email, problems)
            logging.info(f'EasyMon Alerts is going to send the email with details to {to_email}...')
            smtp_server.send_message(msg)
