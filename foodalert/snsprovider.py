import boto3
import json

from django.conf import settings

from dbmail.providers.prowl.push import from_unicode
from botocore.exceptions import BotoCoreError
from datetime import datetime


def format_message(message):
    event = message['event']
    foods = message['food']['served']
    for food in message['foodServiceInfo']['safeToShareFood']:
        food += ' ' + food
    text = "A new Hungry Husky Event: '" + event + "' has been posted! \n"
    time = message['time']['ended']
    details = {
        'Food Served:': message['food']['served'],
        'Location:': message['location'],
        'Amount Left:': message['food']['amount'],
        'Ends At:': time,
    }
    for title, desc in details.items():
        text += title + ' ' + desc + '\n'
    if len(message['food']['allergens']) > 0:
        text += 'Food Contains:'
        for allergen in message['food']['allergens']:
            text += ' ' + allergen
        text += '\n'
    if message['bringContainers']:
        text += 'Please bring a container!'

    return text


def send(recipient, message, **kwargs):
    sender = AmazonSNSProvider()
    return sender.send_message(message, recipient, **kwargs)


class AmazonSNSError(Exception):
    pass


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
                    Subject='Hungry Husky Event',
                )
                successful.append(response)
            except Exception as error:
                failed.append(error.response)

        return {'failed': failed, 'successful': successful}
