import boto3
import json

from django.conf import settings

from dbmail.providers.prowl.push import from_unicode

def send(recipient, message, **kwargs):
    sender = AmazonSNSProvider()
    return sender.send_message(message, **kwargs)


class AmazonSNSError(Exception):
    pass


class AmazonSNSProvider(object):
    client = boto3.client('sns',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name='us-west-2')

    def send_message(self, sms_message):
        message = json.dumps({ 'default': json.dumps(sms_message),
                            'sms': json.dumps(sms_message) })

        response = self.client.publish(
            TopicArn=settings.AWS_TOPIC_ARN,
            Message=message,
            Subject='Hungry Husky Event',
            MessageStructure='json',
        )
        if 'MessageId' not in response:
            raise AmazonSNSError(response)

        return response
