from django.test import TestCase, Client
from foodalert.test.test_notification import NotificationTest
from foodalert.test.test_subscription import SubscriptionTest
from foodalert.test.test_update import UpdateTest
from foodalert.test.test_sms import SMSTest

# Create your tests here.


class ViewTests(TestCase):
    client = Client()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)
