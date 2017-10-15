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

""" Templates for email sent from raceup """

import os
from datetime import datetime
from email.mime.text import MIMEText

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = os.path.join(THIS_FOLDER, "data")
EMAILS_FOLDER = os.path.join(DATA_FOLDER, "emails")
EMAIL_FOOTER_FILE = os.path.join(DATA_FOLDER, "email_footer.txt")
RECIPIENTS_FOLDER = os.path.join(DATA_FOLDER, "address_book")
TODAY = datetime.now().strftime("%A, %d %B %Y")


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


class EmailTemplate(object):
    """ Default email template """

    def __init__(self, recipient, subject, content_file,
                 footer_file=EMAIL_FOOTER_FILE):
        """
        :param recipient: str
            Name and surname of email recipient
        :param subject: str
            Title of email
        :param content_file: str
            Path to file containing email actual content
        :param footer_file: str
            Path to file containing email footer (ending)
        """

        object.__init__(self)

        self.recipient = str(recipient).title().strip()
        self.email_subject = subject
        self.content_file = str(content_file)
        self.footer_file = str(footer_file)

    def get_email_header(self):
        """
        :return: str
            Email header
        """

        return "<h2>Ciao " + str(self.recipient).title() + "!</h2><br>"

    def get_email_footer(self):
        """
        :return: str
            Email text (html formatted)
        """

        return get_email_content(self.footer_file)

    def get_mime_message(self):
        """
        :return: MIMEText
            Email formatted as HTML ready to be sent
        """

        message = MIMEText(
            "<html>" +
            self.get_email_header() +
            get_email_content(self.content_file) +
            self.get_email_footer() +
            "</html>", "html"
        )
        message["subject"] = self.email_subject
        return message


class CVRemainder(EmailTemplate):
    """ Email template to remind candidates to send their CVs """

    def __init__(self, recipient, content_file):
        """
        :param recipient: str
            Name and surname of email recipient
        """

        EmailTemplate.__init__(
            self,
            recipient,
            "Race UP remainder",
            content_file
        )


class MailingList(EmailTemplate):
    """ Email template for classical Race Up newsletter """

    def __init__(self, recipient, content_file):
        """
        :param recipient: str
            Name and surname of email recipient
        :param content_file: str
            Path to file containing email actual content
        """

        EmailTemplate.__init__(
            self,
            recipient,
            "Race UP | Mailing list of " + TODAY,
            content_file
        )


class JobInterview(EmailTemplate):
    """ Email template to notify candidates about time and place of their
    interview """

    def __init__(self, recipient, content_file, date, time, place):
        """
        :param recipient: str
            Name and surname of email recipient
        :param content_file: str
            Path to file containing email actual content
        """

        EmailTemplate.__init__(
            self,
            recipient,
            "Race Up | Colloquio",
            content_file
        )

        self.date = str(date)
        self.time = str(time)
        self.place = str(place)

    def get_email_header(self):
        """
        :return: str
            Email header
        """

        text = "<h2>Ciao " + str(self.recipient).title() + "!</h2><br>"
        text += "a seguito della tua domanda per l'ingresso nel Race UP Team," \
                "ti comunichiamo che il colloquio si terrà il " + "<b>" + \
                self.date + "</b> alle ore <b>" + self.time + "</b> in <b>" \
                + self.place + "</b>.<br>"
        return text
