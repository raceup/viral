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
DATA_FILE_PATH = os.path.join(THIS_FOLDER, "data.csv")
SEND_EMAIL_FROM = "bot.raceup@gmail.com"
TODAY = datetime.now().strftime("%A, %d %B %Y")


class Mailer(object):
    """ Candidate data """

    def __init__(self, raw_dict):
        """
        :param raw_dict: {}
            Raw dict with values
        """

        self.data = raw_dict
        self.name_surname = self.data["Nome"] + " " + self.data["Cognome"]

    def get_notification_msg(self):
        """
        :return: MIMEText
            Personalized message to notify candidates
        """

        message = MIMEText(
            "<html>" +
            "<h2>Ciao " + self.name_surname + "!</h2>" +
            "<p>" +
            "Sono il bot di Race Up, e questa è la nostra mailing list<br>" +
            "Ti scrivo per {...}!<br>" +
            "Sperando di {...},<br>" +
            "<br>" +
            "<i>Il bot di Race Up</i><br>" +
            "<br>" +
            "<i>Race UP team</i><br>" +
            "<a href=\"https://twitter.com/RaceUpTeam\">Twitter</a> | " +
            "<a href=\"https://www.facebook.com/Race-UP-Team-Combustion"
            "-440618820789/\">Facebook CD</a> | " +
            "<a href=\"https://www.facebook.com/Race-UP-Team-Electric"
            "-802147286569414/\"\">Facebook ED</a><br>" +
            "<a href=\"https://www.instagram.com/race_up_team/\">Instagram"
            "</a> | " +
            "<a href=\"https://www.youtube.com/user/teamraceup\">Youtube</a"
            "><br>" +
            "<a href=\"https://it.linkedin.com/grps/Race-Up-Team-3555234"
            "/about?\">Linkedin</a> | " +
            "<a href=\"https://github.com/raceup\">Github</a> | " +
            "<a href=\"mailto:info@raceup.it\">Email</a>" +
            "</p>" +
            "</html>", "html"
        )  # create message

        message["to"] = self.data["Email"]  # email recipient
        message["subject"] = "Race Up | Mailing list " + TODAY

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
            SEND_EMAIL_FROM,
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


def send_notifications():
    """
    :return: void
        Runs bot
    """

    mailers = parse_data(DATA_FILE_PATH)
    for mailer in mailers:
        mailer = Mailer(mailer)  # parse raw csv data
        mailer.notify()
        print("notified " + mailer.name_surname)


if __name__ == '__main__':
    send_notifications()
