import os
import json
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.db import connection
from foodalert.snsprovider import send

class SMSTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipients = ['javerage@uw.edu']

    @classmethod
    def tearDownClass(cls):
        cls.recipients = ''

    def test_send_sms_basic(self):
        """
        Basic test of sending an sms message using the
        AmazonSNS provider
        """

        message = "Hungry Husky Event: Test Event is Open"

        response = send(self.recipients, message)

    def test_send_sms_json(self):
        """
        Basic test of sending a sms message using the
        AmazonSNS provider with json format
        """

        message = {
            'Hungry Husky Event': 'Test Event has opened'
        }

        response = send(self.recipients, message)
