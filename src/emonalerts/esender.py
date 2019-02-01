#!/usr/bin/env python
"""
Esender - email sender
"""

import json
import logging
import subprocess

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
    # Create a secure SSL context
    context = ssl.create_default_context()

    with SMTP_SSL(
        host=smtp_settings['host'],
        port=smtp_settings['port'],
        context=context
    ) as smtp_server:
        smtp_server.login(smtp_settings['email'], smtp_settings['password'])
        if verbose:
            logger.info(f"EasyMon Alerts logged into {smtp_settings['host']} successfully!")
            smtp_server.set_debuglevel(1)

        for to_email in to_emails:
            msg = get_email_message(smtp_settings['email'], to_email, problems)
            logger.info(f'EasyMon Alerts is going to send the email with details to {to_email}...')
            smtp_server.send_message(msg)

def send_via_terminal(to_emails, problems):
    message = """From: EMonAlerts
To: {to_email}
Subject: "{subject}"
Content-Type: text/html
MIME-Version: 1.0

<html>
<body>
    <h1>Problems?</h1>
    {problems}
</body>
</html>
"""
    subject = funny_emos.get_msg_subject() #"You've recieved the alert from EasyMonAlerts"
    logger.info(to_emails)
    for to_email in to_emails:
        with open('/tmp/message.html', 'w') as femail:
            femail.write(message.format(
                to_email=to_email,
                subject=subject,
                problems=problems
            ))

        logger.info(f'EasyMon Alerts is going to send the email via terminal to {to_email}...')
        with open("/tmp/message.html", 'r') as ftmp:
            subprocess.run(["sendmail", "-t"], stdin=ftmp, stdout=subprocess.PIPE)