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

from hal.internet.email.templates import EmailTemplate
from hal.time.dates import get_next_weekday, Weekday

THIS_FOLDER = os.path.dirname(os.path.realpath(__file__))
DATA_FOLDER = os.path.join(THIS_FOLDER, "data")
EMAILS_FOLDER = os.path.join(DATA_FOLDER, "emails")
EMAIL_FOOTER_FILE = os.path.join(DATA_FOLDER, "email_footer.txt")
RECIPIENTS_FOLDER = os.path.join(DATA_FOLDER, "address_book")
TODAY = datetime.now().strftime("%A, %d %B %Y")


class CVRemainder(EmailTemplate):
    """ Email template to remind candidates to send their CVs """

    def __init__(self, recipient, content_file, extra_args=None):
        """
        :param recipient: str
            Name and surname of email recipient
        :param extra_args: {}
            Extra arguments and details about recipient
        """

        EmailTemplate.__init__(
            self,
            recipient,
            "Race UP remainder",
            content_file,
            EMAIL_FOOTER_FILE,
            extra_args=extra_args
        )


class MailingList(EmailTemplate):
    """ Email template for classical Race Up newsletter """

    def __init__(self, recipient, content_file, extra_args=None):
        """
        :param recipient: str
            Name and surname of email recipient
        :param content_file: str
            Path to file containing email actual content
        :param extra_args: {}
            Extra arguments and details about recipient
        """

        EmailTemplate.__init__(
            self,
            recipient,
            "Race UP | Mailing list of " + TODAY,
            content_file,
            EMAIL_FOOTER_FILE,
            extra_args=extra_args
        )


class JobInterview(EmailTemplate):
    """ Email template to notify candidates about time and place of their
    interview """

    def __init__(self, recipient, content_file, extra_args):
        """
        :param recipient: str
            Name and surname of email recipient
        :param content_file: str
            Path to file containing email actual content
        :param extra_args: {}
            Details about date, time and place of the interview
        """

        EmailTemplate.__init__(
            self,
            recipient,
            "Race Up | Colloquio",
            content_file,
            EMAIL_FOOTER_FILE,
            extra_args=extra_args
        )

        self.date = self.data["Data"]
        self.time = self.data["Ora"]
        self.place = self.data["Luogo"]

    def get_email_header(self):
        """
        :return: str
            Email header
        """

        text = "<h2>Ciao " + str(self.recipient).title() + "!</h2><br>"
        text += "a seguito della tua domanda per l'ingresso nel Race UP Team," \
                " ti comunichiamo che il colloquio si terrà il " + "<b>" + \
                self.date + "</b> alle ore <b>" + self.time + "</b> in <b>" \
                + self.place + "</b>.<br>"
        return text


class CakeRemainder(EmailTemplate):
    """ Email template to notify Race Up members to bring a slice of cake
    on weekly saturday meetings """

    def __init__(self, recipient, content_file, extra_args=None):
        """
        :param recipient: str
            Name and surname of email recipient
        :param content_file: str
            Path to file containing email actual content
        :param extra_args: {}
            Details about next meeting date
        """

        EmailTemplate.__init__(
            self,
            recipient,
            "Race Up | Il bot delle torte",
            content_file,
            EMAIL_FOOTER_FILE,
            extra_args=extra_args
        )

    def get_email_header(self):
        """
        :return: str
            Email header
        """

        date_remainder = get_next_weekday(Weekday.SATURDAY)
        text = "<h2>Ciao " + str(self.recipient).title() + "!</h2><br>"
        text += "<br>Ti scrivo per ricordarti di portare almeno una torta "
        text += " il prossimo sabato " + str(date_remainder) + " in OZ!<br>"
        return text


class JobInterviewResult(EmailTemplate):
    """ Email template to notify candidates about the result of their
    interview """

    def __init__(self, recipient, content_folder, extra_args):
        """
        :param recipient: str
            Name and surname of email recipient
        :param content_folder: str
            Path to folder containing possible answers
        :param extra_args: {}
            Details about date, time and place of the interview
        """

        EmailTemplate.__init__(
            self,
            recipient,
            "Race Up | Esito colloquio",
            JobInterviewResult.get_content_file_from_result(
                content_folder, extra_args["Tipo risposta"]
            ),
            EMAIL_FOOTER_FILE,
            extra_args=extra_args
        )

    def get_email_header(self):
        """
        :return: str
            Email header
        """

        return "<h4>Caro/a " + str(self.recipient).title() + ",</h4><br>"

    @staticmethod
    def get_content_file_from_result(folder, result):
        """
        :param folder: str
            Path to folder containing possible answers
        :param result: str
            Result of interview (as in .csv file)
        :return: str
            Path to content file
        """

        return os.path.join(
            folder,
            str(result).strip() + ".txt"
        )
