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
import csv
import time

import templates
from emails import Recipient

EMAIL_TEMPLATES = {
    "mailing list": templates.MailingList,
    "cv remainder": templates.CVRemainder,
    "colloquio": templates.JobInterview,
    "cakes": templates.CakeRemainder,
    "esito": templates.JobInterviewResult
}
TIME_INTERVAL_BETWEEN_EMAILS = 1  # seconds to wait before sending next email


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
                "Cognome"].title() + " (" + recipient["Email"] + ")"
            for recipient in recipients
            ]
    ))
    print("\nwith content from >>> '", email_text_file, "'")
    return input("\nAre you really sure? [y/n] ").startswith("y")


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

    recipients = list(parse_data(addresses_file))
    if confirm_send_notifications(recipients, email_text_file):
        for recipient in recipients:
            name_surname = recipient["Nome"].title() + " " + recipient[
                "Cognome"].title()

            template = email_template(
                name_surname,
                email_text_file,
                extra_args=recipient
            )  # create email template specific for this user
            recip = Recipient(recipient, template)
            print(
                "Notifying", name_surname, "..."
            )  # notify user
            recip.notify()
            print(
                "\t ... sent email to", recipient["Email"]
            )  # notify user
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
