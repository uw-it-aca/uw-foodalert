import os
from unittest.mock import patch, Mock, PropertyMock

from django.test import TestCase, Client
from django.test.utils import override_settings
from django.db import connection
from django.conf import settings

from twilio.base.exceptions import TwilioRestException
from twilio.twiml.messaging_response import MessagingResponse

from foodalert.sender import TwilioSender, Sender
from foodalert.models import Subscription
from foodalert.test.test_utils import create_user_from_data,\
    generate_twilio_request_validator_mock


class TwilioTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.recipients = ['+11111111111']
        cls.message = "UW Food Alert Event: Test Event is Open"

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
            sms = Sender.send_twilio_sms(self.recipients, self.message)
            self.assertEquals('UW Food Alert Event: Test Event is Open',
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
            sms = Sender.send_twilio_sms(recipients, self.message)
            self.assertEquals(400, sms.status)

    @override_settings(TWILIO_ACCOUNT_SID="test_sid")
    def test_reply_verify_yes(self):
        """
        Tests replies recivied form twilio
        """
        sub_user = create_user_from_data({
            "username": "test_sub",
            "email": "test_sub@uw.edu",
            "password": "test_password"
        })
        sub = Subscription.objects.create(
            user=sub_user,
            email=sub_user.email,
            sms_number="+41524204242"
        )

        with generate_twilio_request_validator_mock():
            client = Client()
            response = client.post('/sms/', data={
                'AccountSid': 'test_sid',
                'From': str(sub.sms_number),
                'Body': 'YES'
            }, HTTP_X_TWILIO_SIGNATURE='unknown_value')
            self.assertEqual(response.status_code, 200)

            sub.refresh_from_db()
            self.assertTrue(sub.number_verified)

        sub.delete()
        sub_user.delete()

    @override_settings(TWILIO_ACCOUNT_SID="test_sid")
    def test_reply_resume(self):
        """
        Tests replies recivied form twilio
        """
        sub_user = create_user_from_data({
            "username": "test_sub",
            "email": "test_sub@uw.edu",
            "password": "test_password"
        })
        sub = Subscription.objects.create(
            user=sub_user,
            email=sub_user.email,
            sms_number="+41524204242",
            number_verified=True
        )

        with generate_twilio_request_validator_mock():
            client = Client()
            response = client.post('/sms/', data={
                'AccountSid': 'test_sid',
                'From': str(sub.sms_number),
                'Body': 'RESUME'
            }, HTTP_X_TWILIO_SIGNATURE='unknown_value')
            self.assertEqual(response.status_code, 200)

            sub.refresh_from_db()
            self.assertTrue(sub.send_sms)

        sub.delete()
        sub_user.delete()

    @override_settings(TWILIO_ACCOUNT_SID="test_sid")
    def test_reply_pause(self):
        """
        Tests replies recivied form twilio
        """
        sub_user = create_user_from_data({
            "username": "test_sub",
            "email": "test_sub@uw.edu",
            "password": "test_password"
        })
        sub = Subscription.objects.create(
            user=sub_user,
            email=sub_user.email,
            sms_number="+41524204242",
            number_verified=True,
            send_sms=True
        )

        with generate_twilio_request_validator_mock():
            client = Client()
            response = client.post('/sms/', data={
                'AccountSid': 'test_sid',
                'From': str(sub.sms_number),
                'Body': 'PAUSE'
            }, HTTP_X_TWILIO_SIGNATURE='unknown_value')
            self.assertEqual(response.status_code, 200)

            sub.refresh_from_db()
            self.assertFalse(sub.send_sms)

        sub.delete()
        sub_user.delete()

    @override_settings(TWILIO_ACCOUNT_SID="test_sid")
    def test_reply_unknown(self):
        """
        Tests replies recivied form twilio
        """
        sub_user = create_user_from_data({
            "username": "test_sub",
            "email": "test_sub@uw.edu",
            "password": "test_password"
        })
        sub = Subscription.objects.create(
            user=sub_user,
            email=sub_user.email,
            sms_number="+41524204242"
        )

        with generate_twilio_request_validator_mock():
            client = Client()
            response = client.post('/sms/', data={
                'AccountSid': 'test_sid',
                'From': str(sub.sms_number),
                'Body': 'TEST_MESSAGE'
            }, HTTP_X_TWILIO_SIGNATURE='unknown_value')
            self.assertEqual(response.status_code, 200)

            sub_updated = Subscription.objects.get(pk=sub.pk)
            self.assertEqual(sub_updated.sms_number, sub.sms_number)
            self.assertEqual(sub_updated.number_verified, sub.number_verified)
            self.assertEqual(sub_updated.send_sms, sub.send_sms)

        sub.delete()
        sub_user.delete()

    @override_settings(TWILIO_ACCOUNT_SID="test_sid")
    def test_reply_wrong_number(self):
        """
        Tests replies recivied form twilio
        """
        sub_user = create_user_from_data({
            "username": "test_sub",
            "email": "test_sub@uw.edu",
            "password": "test_password"
        })
        sub = Subscription.objects.create(
            user=sub_user,
            email=sub_user.email,
            sms_number="+41524204242"
        )

        with generate_twilio_request_validator_mock():
            client = Client()
            response = client.post('/sms/', data={
                'AccountSid': 'test_sid',
                'From': "+41524204243",
                'Body': 'YES'
            }, HTTP_X_TWILIO_SIGNATURE='unknown_value')
            self.assertEqual(response.status_code, 200)

            resp = MessagingResponse()
            resp.message('UW Food Alert does not have this number registered.')
            self.assertEqual(response.content.decode("utf-8"), str(resp))

            sub_updated = Subscription.objects.get(pk=sub.pk)
            self.assertEqual(sub_updated.sms_number, sub.sms_number)
            self.assertEqual(sub_updated.number_verified, sub.number_verified)
            self.assertEqual(sub_updated.send_sms, sub.send_sms)

        sub.delete()
        sub_user.delete()
