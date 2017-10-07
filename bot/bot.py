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


import base64
import csv
import os
from datetime import datetime
from email.mime.text import MIMEText

from google import gauthenticator

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = os.path.join(THIS_FOLDER, "data")
TODAY = datetime.now().strftime("%A, %d %B %Y")
EMAIL_TITLE = "Race UP remainder"  # below are email-related settings
EMAIL_ADDRESSES_FILE = os.path.join(DATA_FOLDER, "send_to.csv")
EMAIL_TEXT_FILE = os.path.join(DATA_FOLDER, "email_text.txt")
EMAIL_FOOTER_FILE = os.path.join(DATA_FOLDER, "email_footer.txt")
SEND_EMAIL_FROM = "info@raceup.it"


def get_email_header(name_surname):
    """
    :param name_surname: str
        Name and surname of email receiver
    :return: str
        Email header
    """

    return "<h2>Ciao " + str(name_surname).title() + "!</h2>"


def get_email_content(file_path):
    """
    :param file_path: str
        Path to file with email text
    :return: str
        Email text (html formatted)
    """

    with open(file_path, "r") as in_file:
        text = str(in_file.read())
        return text.replace("\n", "<br>")


def get_email_footer(file_path=EMAIL_FOOTER_FILE):
    """
    :param file_path: str
        Path to file with email text
    :return: str
        Email text (html formatted)
    """

    return get_email_content(file_path)


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


class Mailer(object):
    """ Candidate data """

    def __init__(self, raw_dict):
        """
        :param raw_dict: {}
            Raw dict with values
        """

        self.data = raw_dict
        self.name_surname = self.data["Nome"].title() + " " + self.data[
            "Cognome"].title()
        self.email = self.data["Email"].strip()

    def get_notification_msg(self, email_text_file):
        """
        :param email_text_file: str
            File to get email text from
        :return: MIMEText
            Personalized message to notify candidates
        """

        message = MIMEText(
            "<html>" +
            get_email_header(self.name_surname) +
            get_email_content(email_text_file) +
            get_email_footer() +
            "</html>", "html"
        )  # create message

        message["to"] = self.email  # email recipient
        message["subject"] = EMAIL_TITLE

        return {
            "raw": base64.urlsafe_b64encode(message.as_bytes()).decode()
        }

    def notify(self, email_text_file):
        """
        :param email_text_file: str
            File to get email text from
        :return: bool
            Sends me a message if today is my birthday.
            Returns true iff sent message
        """

        send_email(
            SEND_EMAIL_FROM,
            self.get_notification_msg(email_text_file)
        )


def confirm_send_notifications(mailers, email_text_file):
    """
    :param mailers: [] of Mailer
        List of email receivers
    :param email_text_file: str
        File to get email text from
    :return: bool
        True iff user really wants to send emails
    """

    print("Sending emails to\n")
    print("\n".join(
        [
            ">>> " + mailer.name_surname + " ( " + mailer.email + " )"
            for mailer in mailers
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

    mailers = parse_data(EMAIL_ADDRESSES_FILE)
    mailers = [Mailer(mailer) for mailer in mailers]  # parse raw csv data
    if confirm_send_notifications(mailers, email_text_file):
        for mailer in mailers:
            mailer.notify(email_text_file)
            print("Sent email to", mailer.name_surname, "(", mailer.email, ")")
    else:
        print("Aborting")

if __name__ == '__main__':
    send_notifications(EMAIL_TEXT_FILE)
