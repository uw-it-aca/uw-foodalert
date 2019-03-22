import os
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.db import connection
from django.conf import settings
from foodalert.twilio_sender import TwilioSender, send
from unittest.mock import patch, Mock, PropertyMock
from twilio.base.exceptions import TwilioRestException


class TwilioTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipients = ['+11111111111']
        cls.message = "Hungry Husky Event: Test Event is Open"

    @classmethod
    def tearDownClass(cls):
        cls.recipients = ''
        cls.message = ''

    def test_send_sms_basic_mock(self):
        """
        Basic test of sending an sms message using the
        Twilio Sender and a mocked Twilio Client
        """
        ret = Mock()
        ret.body = self.message
        ret.status = 200
        m2 = Mock()
        m2.notifications = Mock()
        m2.notifications.create = PropertyMock(return_value=ret)

        m1 = Mock()
        m1.notify = Mock()
        m1.notify.services = PropertyMock(return_value=m2)

        with patch.object(
                         TwilioSender,
                         'c',
                         new_callable=PropertyMock) as mock:
            mock.return_value = m1
            sms = send(self.recipients, self.message)
            self.assertEquals('Hungry Husky Event: Test Event is Open',
                              sms.body)
            self.assertEquals(200, sms.status)

    def test_send_invalid_recipients(self):
        """
        Basic test of sending ansms message through
        the Twilio Sender with invalid recipients
        """
        ret = Mock()
        ret.status = 400
        m2 = Mock()
        m2.notifications = Mock()
        m2.notifications.create = PropertyMock(return_value=ret)

        m1 = Mock()
        m1.notify = Mock()
        m1.notify.services = PropertyMock(return_value=m2)

        with patch.object(
                         TwilioSender,
                         'c',
                         new_callable=PropertyMock) as mock:
            mock.return_value = m1
            recipients = ['']
            sms = send(recipients, self.message)
            self.assertEquals(400, sms.status)
