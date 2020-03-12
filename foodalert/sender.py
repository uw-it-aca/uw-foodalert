import json

from dbmail import send_db_mail
from dbmail.models import MailTemplate
from django.conf import settings
import boto3
from twilio.rest import Client
import dateutil.parser
import datetime
from django.utils import timezone


class Sender:
    def send_email(body, recipients, time, location, event):
        email_name = "Food Alert "
        email_subject = "[UW Food Alert] "

        if body[:6] == 'Update':
            email_name += "Update"
            email_subject += "Update: {}, {}".format(event, location)
        else:
            email_name += "Notification"
            email_subject += "Food Available: {}, {}".format(event, location)

        MailTemplate.objects.create(
            name=email_name,
            subject=email_subject,
            message=body,
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

    def send_amazon_sms(recipient, message, **kwargs):
        sender = AmazonSNSProvider()
        return sender.send_message(message, recipient, **kwargs)

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
            raise ImproperlyConfigured("You haven't set
                                       'TWILIO_NOTIFY_SERVICE_ID'.")

        sms = self.c.notify.services(twilio_notify_service_id) \
                    .notifications.create(
                        body=message,
                        to_binding=bindings
                    )
        return sms


class AmazonSNSProvider(object):
    def __init__(self):
        aws_key_id = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
        aws_secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)
        if aws_key_id is None:
            raise ImproperlyConfigured("You haven't set 'AWS_ACCESS_KEY_ID'.")
        if aws_secret_key is None:
            raise ImproperlyConfigured("You haven't set
                                       'AWS_SECRET_ACCESS_KEY'.")

        self.client = boto3.client(
            'sns',
            aws_access_key_id=aws_key_id,
            aws_secret_access_key=aws_secret_key,
            region_name='us-west-2'
        )

    def send_message(self, sms_message, recipients):
        failed = []
        successful = []

        for recipient in recipients:
            try:
                response = self.client.publish(
                    PhoneNumber=recipient,
                    Message=sms_message,
                    Subject='UW Food Alert Event',
                )
                successful.append(response)
            except Exception as error:
                failed.append(error.response)

        return {'failed': failed, 'successful': successful}


class AmazonSNSError(Exception):
    pass
