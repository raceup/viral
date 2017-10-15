# !/usr/bin/python
# coding: utf_8

# Copyright 2017-2018 Race UP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Sends emails from raceup """

import base64
import csv
import os

from . import templates
from .google import gauthenticator

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = os.path.join(THIS_FOLDER, "data")
EMAILS_FOLDER = os.path.join(DATA_FOLDER, "emails")
EMAIL_ADDRESSES_FILE = os.path.join(EMAILS_FOLDER, "cv_remainder.csv")
EMAIL_TEXT_FILE = os.path.join(EMAILS_FOLDER, "cv_remainder.txt")
SENDER = "info@raceup.it"
EMAIL_TEMPLATES = {
    "0": templates.MailingList,
    "1": templates.CVRemainder
}


class Recipient(object):
    """ Candidate data """

    def __init__(self, raw_dict, email_template):
        """
        :param raw_dict: {}
            Raw dict with values
        :param email_text_file: str
            File to get email text from
        """

        self.data = raw_dict
        self.email = self.data["Email"].strip()
        self.email_template = email_template

    def get_notification_msg(self):
        """
        :return: MIMEText
            Personalized message to notify candidates
        """

        message = self.email_template.get_mime_message()
        message["to"] = self.email  # email recipient

        return {
            "raw": base64.urlsafe_b64encode(message.as_bytes()).decode()
        }

    def notify(self):
        """
        :return: bool
            Sends me a message if today is my birthday.
            Returns true iff sent message
        """

        send_email(
            SENDER,
            self.get_notification_msg()
        )


def send_email(sender, msg):
    """
    :param sender: str
        Sender of email
    :param msg: str
        Message to send to me
    :return: void
        Sends email to me with this message
    """

    service = gauthenticator.create_gmail_driver()
    service.users().messages().send(
        userId=sender,
        body=msg
    ).execute()  # send message


def parse_data(file_path):
    """
    :param file_path: str
        Path to file to parse
    :return: (generator of) [] of {}
        List of items in data with specified attrs
    """

    reader = csv.DictReader(open(file_path, "r"))
    for row in reader:
        if row:
            yield row


def confirm_send_notifications(recipients, email_text_file):
    """
    :param recipients: [] of Mailer
        List of email receivers
    :param email_text_file: str
        File to get email text from
    :return: bool
        True iff user really wants to send emails
    """

    print("Sending emails to\n")
    print("\n".join(
        [
            ">>> " + recipient["Nome"].title() + " " + recipient[
                "Cognome"].title() + " ( " + recipient["email"] + " )"
            for recipient in recipients
            ]
    ))
    print("\nwith the following content:\n")
    file_content = open(email_text_file, "r").read()
    print(">>>", file_content.replace("\n", "\n>>> "))  # read file
    return input("\nAre you really sure? [y/n] ").startswith("y")


def send_notifications(email_text_file):
    """
    :param email_text_file: str
        File to get email text from
    :return: void
        Runs bot
    """

    recipients = parse_data(EMAIL_ADDRESSES_FILE)
    if confirm_send_notifications(recipients, email_text_file):
        for recipient in recipients:
            name_surname = recipient["Nome"].title() + " " + recipient[
                "Cognome"].title()
            template = templates.MailingList(
                name_surname,
                email_text_file
            )
            Recipient(recipient, template).notify()
            print(
                "Sent email to", name_surname, "(", recipient["email"], ")"
            )  # notify user
    else:
        print("Aborting")

if __name__ == '__main__':
    send_notifications(
        EMAIL_TEXT_FILE
    )
