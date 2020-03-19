from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.core.exceptions import ImproperlyConfigured

from foodalert.sender import TwilioSender


class MissingSettingTest(TestCase):
    @override_settings()
    def test_delete_twilio_notify_service_id(self):
        del settings.TWILIO_NOTIFY_SERVICE_ID

        with self.assertRaises(ImproperlyConfigured) as exp:
            TwilioSender().send_message([+11111111111], 'hello')
        self.assertEqual(str(exp.exception),
                         ("You haven't set 'TWILIO_NOTIFY_SERVICE_ID'."))
