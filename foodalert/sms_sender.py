import boto3
import json

from django.conf import settings
from dbmail import send_db_sms
from dbmail.providers.prowl.push import from_unicode
from twilio.rest import Client

class SMS_Sender(object):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    def send_message(recipients, message, **kwargs)
        sms = client.messages \
                    .create(
                        body=message,
                        from_=settings.TWILIO_FROM
                        to=recipients
                    )
        print(sms.sid)              
