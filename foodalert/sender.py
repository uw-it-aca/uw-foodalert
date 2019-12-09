import json

from dbmail import send_db_mail
from dbmail.models import MailTemplate
from django.conf import settings
import boto3
from twilio.rest import Client
import dateutil.parser
from datetime import datetime


class Sender:
    def send_email(body, recipients, time, location):
        email_name = "Food Alert "
        email_subject = "[UW Food Alert] "

        if body[:6] == 'Update':
            email_name += "Update"
            email_subject += "Update for Food in " + location
        else:
            email_name += "Notification"
            email_subject += "Food Available in " + location

        MailTemplate.objects.create(
            name=email_name,
            subject=email_subject,
            message=body,
            slug=time,
            is_html=False,
        )

        send_db_mail(
            slug=time,
            recipient=settings.SAFE_EMAIL_RECIPIENT,
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

        text = "Food leftover from " + event + ".\n\n"
        time = datetime.strftime(message['time']['end'], "%I:%M %p")

        details = {
            'Food served:': foods,
            'End time:': time,
            'Location:': message['location'],
        }
        for title, desc in details.items():
            text += title + ' ' + desc + '\n'
        if len(message['food']['allergens']) > 0:
            text += 'May contain: '
            for allergen in message['food']['allergens']:
                text += allergen + ", "
            text = text[:-2]
            text += '\n\n'
        if message['bring_container']:
            text += 'You must bring a container.\n\n'

        text += 'Thanks,\n'
        text += 'UW Food Alert'

        return text


class TwilioSender(object):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
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

        sms = self.c.notify.services(settings.TWILIO_NOTIFY_SERVICE_ID) \
                    .notifications.create(
                        body=message,
                        to_binding=bindings
                    )
        return sms


class AmazonSNSProvider(object):
    def __init__(self):
        self.client = boto3.client(
            'sns',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
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
