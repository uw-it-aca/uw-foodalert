# Copyright 2023 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
import json

from dbmail import send_db_mail
from dbmail.models import MailTemplate
from django.conf import settings
import boto3
from twilio.rest import Client
import dateutil.parser
import datetime
from django.utils import timezone

from django.core.exceptions import ImproperlyConfigured


class Sender:
    def send_email(email, recipients, time):
        MailTemplate.objects.create(
            name=email['name'],
            subject=email['subject'],
            message=email['body'],
            slug=time,
            is_html=False,
        )

        send_db_mail(
            slug=time,
            recipient=[],
            bcc=recipients,
            use_celery=False
        )

    def send_twilio_sms(recipient, message, **kwargs):
        sender = TwilioSender()
        return sender.send_message(recipient, message, **kwargs)

    def format_message(message):
        event = message['event']
        foods = message['food']['served']

        text = "Food available: {}\n".format(event)
        text += "{}\n\n".format(foods)

        local_time = timezone.localtime(message['time']['end'])
        formatted_time = local_time.strftime("%I:%M %p")

        details = {
            'End time:': formatted_time,
            'Location:': message['location'],
        }
        for title, desc in details.items():
            text += "{} {}\n".format(title, desc)
        if len(message['food']['allergens']) > 0:
            text += 'May contain: '
            for allergen in message['food']['allergens']:
                text += "{}, ".format(allergen)
            text = text[:-2]
            text += '\n'
        text += '\n'
        if message['bring_container']:
            text += 'You must bring a container.\n\n'

        text += 'Thanks,\n'
        text += 'UW Food Alert'

        return text


class TwilioSender(object):
    account_sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
    auth_token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
    if account_sid is None:
        raise ImproperlyConfigured("You haven't set 'TWILIO_ACCOUNT_SID'.")
    if auth_token is None:
        raise ImproperlyConfigured("You haven't set 'TWILIO_AUTH_TOKEN'.")

    c = Client(account_sid, auth_token)

    def send_message(self, recipients, message):
        bindings = []
        for recipient in recipients:
            bindings.append(json.dumps(
                {
                    "binding_type": "sms",
                    "address": recipient
                }
            ))

        twilio_notify_service_id = \
            getattr(settings, 'TWILIO_NOTIFY_SERVICE_ID', None)
        if twilio_notify_service_id is None:
            raise ImproperlyConfigured("You haven't set " +
                                       "'TWILIO_NOTIFY_SERVICE_ID'.")

        sms = self.c.notify.services(twilio_notify_service_id) \
                    .notifications.create(
                        body=message,
                        to_binding=bindings
                    )
        return sms
