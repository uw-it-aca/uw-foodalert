import os
from unittest.mock import patch, Mock, PropertyMock

from django.test import TestCase, Client
from django.test.utils import override_settings
from django.db import connection
from django.conf import settings

from twilio.base.exceptions import TwilioRestException

from foodalert.sender import TwilioSender, Sender
from foodalert.models import Subscription
from foodalert.test.test_utils import create_user_from_data


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
            sms = Sender.send_twilio_sms(self.recipients, self.message)
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
            sms = Sender.send_twilio_sms(recipients, self.message)
            self.assertEquals(400, sms.status)

    @override_settings(TWILIO_ACCOUNT_SID="test_sid")
    def test_reply_verify(self):
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

        client = Client()
        response = client.post('/sms/', data={
            'AccountSid': 'test_sid',
            'From': str(sub.sms_number),
            'Body': 'YES'
        })
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

        client = Client()
        response = client.post('/sms/', data={
            'AccountSid': 'test_sid',
            'From': str(sub.sms_number),
            'Body': 'RESUME'
        })
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

        client = Client()
        response = client.post('/sms/', data={
            'AccountSid': 'test_sid',
            'From': str(sub.sms_number),
            'Body': 'PAUSE'
        })
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

        client = Client()
        response = client.post('/sms/', data={
            'AccountSid': 'test_sid',
            'From': str(sub.sms_number),
            'Body': 'TEST_MESSAGE'
        })
        self.assertEqual(response.status_code, 200)

        sub_updated = Subscription.objects.get(pk=sub.pk)
        self.assertEqual(sub_updated.sms_number, sub.sms_number)
        self.assertEqual(sub_updated.number_verified, sub.number_verified)
        self.assertEqual(sub_updated.send_sms, sub.send_sms)

        sub.delete()
        sub_user.delete()

    @override_settings(TWILIO_ACCOUNT_SID="test_sid")
    def test_reply_wrong_SID(self):
        """
        Tests replies recivied form twilio
        """
        client = Client()
        response = client.post('/sms/', data={})
        self.assertEqual(response.status_code, 403)

        client = Client()
        response = client.post('/sms/', data={
            'AccountSid': 'random value'
        })
        self.assertEqual(response.status_code, 403)
