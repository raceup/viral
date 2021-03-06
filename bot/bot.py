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

import argparse
import time

import templates
from emails import Recipient
from hal.files.parsers import CSVParser
from hal.streams.user import UserInput

EMAIL_TEMPLATES = {
    "mailing list": templates.Newsletter,
    "cv remainder": templates.CVRemainder,
    "colloquio": templates.JobInterview,
    "cakes": templates.CakeRemainder,
    "esito": templates.JobInterviewResult
}
USER_INPUT = UserInput()
TIME_INTERVAL_BETWEEN_EMAILS = 1  # seconds to wait before sending next email


def create_and_parse_args():
    parser = argparse.ArgumentParser(
        usage="-e <EMAIL TEMPLATE> -c <CONTENT FILE> -a <RECIPIENTS FILE>\n"
              "-help for help and usage")
    parser.add_argument("-e", dest="email_template",
                        help="Email template, one in [" + " | ".join(
                            EMAIL_TEMPLATES.keys()) + "]",
                        required=True)
    parser.add_argument("-c", dest="content_file",
                        help="Email content file",
                        required=True)
    parser.add_argument("-a", dest="recipients_file",
                        help="Recipients file (.csv format)", required=True)

    args = parser.parse_args()  # parse args

    return {
        "email_template": EMAIL_TEMPLATES[args.email_template],
        "content_file": args.content_file,
        "recipients_file": args.recipients_file
    }


def get_recipient_contacts(raw_data):
    """
    :param raw_data: {}
        Raw recipient data
    :return: {}
        Dict with email and name of recipient
    """

    email = raw_data["Email"]

    try:
        name_surname = raw_data["Nome"].title() + " " + raw_data[
            "Cognome"].title()
    except:
        name_surname = raw_data["Nome e Cognome"].title()

    return {
        "name": name_surname,
        "email": email
    }


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
            ">>> " + get_recipient_contacts(recipient)["name"] +
            " (" + get_recipient_contacts(recipient)["email"] + ")"
            for recipient in recipients
        ]
    ))
    print("\nwith content from >>> '", email_text_file, "'")
    return USER_INPUT.get_yes_no("\nAre you really sure?")


def send_notifications(addresses_file, email_text_file, email_template):
    """
    :param addresses_file: str
        File to get recipients data from
    :param email_text_file: str
        File to get email text from
    :param email_template: constructor
        Email template to use
    :return: void
        Runs bot
    """

    recipients = list(CSVParser(addresses_file).get_dicts())
    if confirm_send_notifications(recipients, email_text_file):
        for recipient in recipients:
            name_surname = get_recipient_contacts(recipient)["name"]

            template = email_template(
                name_surname,
                email_text_file,
                extra_args=recipient
            )  # create email template specific for this user
            recip = Recipient(recipient, template)
            print(
                "Notifying", name_surname, "..."
            )  # notify user
            try:
                recip.notify()
                print(
                    "\t ... sent email to", recipient["Email"]
                )  # notify user
            except:
                print(
                    "\t CANNOT send email to", recipient["Email"]
                )
            time.sleep(TIME_INTERVAL_BETWEEN_EMAILS)
    else:
        print("Aborting")


def main():
    """
    :return: void
        Sends email with user args
    """

    args = create_and_parse_args()
    send_notifications(
        args["recipients_file"],
        args["content_file"],
        args["email_template"]
    )


if __name__ == '__main__':
    main()
