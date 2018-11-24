#!/usr/bin/env python
"""
Funny emos - funny messages for the whole app with emoji ^_^
"""
import emoji

def first_run(file_path):
    return emoji.emojize(
        f'It looks like your first run :smiling_face_with_smiling_eyes:. Welcome.'
    )

def get_msg_content(problems):
    text = emoji.emojize(':unamused_face: Unfortinatully we have noticed some problems.\n')
    for url in problems:
        text += f'\tURL: {url}\n'
        text += f'\tThe error: {problems[url]}\n\n'
    text += emoji.emojize('We hope this message will help you to understand the problem better. Good luck! :winking_face:\n')
    return text

def get_msg_subject():
    return emoji.emojize("You've recieved the alert from EasyMonAlerts :seven_o’clock:")
