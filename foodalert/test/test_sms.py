import os
import json
from datetime import datetime
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.db import connection
from django.conf import settings
from foodalert.sender import Sender, AmazonSNSProvider
from unittest.mock import patch, Mock


class SMSTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipients = ['+15099693178']
        cls.message = "UW Food Alert Event: Test Event is Open"

    @classmethod
    def tearDownClass(cls):
        cls.recipients = ''
        cls.message = ''

    def test_send_sms_basic(self):
        """
        Basic test of sending an sms message using the
        AmazonSNS provider
        """
        ret = {
            'failed': [],
            'successful': ['test']
        }
        with patch.object(
                AmazonSNSProvider,
                'send_message',
                return_value=ret) as mock:
            response = Sender.send_amazon_sms(self.recipients, self.message)
            mock.assert_called_once()
            self.assertEqual(len(response['failed']), 0)

    @override_settings(AWS_ACCESS_KEY_ID='XXX')
    def test_send_sms_invalid_credentials(self):
        """
        Tests that an exception is thrown when sending to
        an invalid number
        """
        response = Sender.send_amazon_sms(self.recipients, self.message)
        self.assertEqual(len(response['failed']), 1)
        self.assertEqual(response['failed'][0]['Error']['Code'],
                         'InvalidClientTokenId')

    def test_format_message(self):
        """
        Tests the format message function used to format
        a notification instance into a readable text
        """
        data = {
            'location': 'UW Campus',
            'event': 'UW Event',
            'time': {
                'end': datetime.strptime('2019-12-13T20:23:06.200-+0000',
                                         "%Y-%m-%dT%H:%M:%S.%f-%z"),
            },
            'food': {
                'served': 'Sandwitches',
                'allergens': ['wheat', 'fish', 'peanuts']
            },
            'bring_container': True,
        }

        expected = ("Food leftover from UW Event.\n\n"
                    "Food served: Sandwitches\n"
                    "End time: 12:23 PM\n"
                    "Location: UW Campus\n"
                    "May contain: wheat, fish, peanuts\n\n"
                    "You must bring a container.\n\n"
                    "Thanks,\n"
                    "UW Food Alert")

        message = Sender.format_message(data)
        self.assertEquals(message, expected)
