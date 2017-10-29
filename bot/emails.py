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

""" Sends emails from Race Up """

import base64
import os

from hal.internet.email import gmail

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = os.path.join(THIS_FOLDER, "data")
OAUTH_FOLDER = os.path.join(THIS_FOLDER, ".user_credentials", "gmail")
SENDER = "info@raceup.it"
EMAIL_DRIVER = gmail.GMailApiOAuth(
    "Race Up Viral",
    os.path.join(OAUTH_FOLDER, "client_secret.json"),
    os.path.join(OAUTH_FOLDER, "gmail.json")
).create_driver()


class Recipient(object):
    """ Candidate data """

    def __init__(self, raw_dict, email_template):
        """
        :param raw_dict: {}
            Raw dict with values
        :param email_template: EmailTemplate
            Email template to use
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

        send_email(self.get_notification_msg())


def send_email(msg):
    """
    :param msg: str
        Message to send to me
    :return: void
        Sends email to me with this message
    """

    gmail.send_email(
        SENDER,
        msg,
        EMAIL_DRIVER
    )
