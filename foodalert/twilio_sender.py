import json
from django.conf import settings
from dbmail import send_db_sms
from dbmail.providers.prowl.push import from_unicode
from twilio.rest import Client


def send(recipient, message, **kwargs):
    sender = TwilioSender()
    return sender.send_message(recipient, message, **kwargs)


class TwilioSender(object):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    from_number = settings.TWILIO_FROM
    c = Client(account_sid, auth_token)

    def send_message(self, recipients, message):
        bindings = []
        for recipient in recipients:
            bindings.append("{\"binding_type\": \"sms\", \"address\": \"" +
                            recipient + "\"}")

        sms = self.c.notify.services(settings.TWILIO_NOTIFY_SERVICE_ID) \
                    .notifications.create(
                        body=message,
                        to_binding=bindings
                    )
        return sms
