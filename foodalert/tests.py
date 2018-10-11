from django.test import TestCase, Client
from foodalert.test.test_notification import NotificationTest

# Create your tests here.


class DummyTests(TestCase):
    def test_one_plus_one_is_two(self):
        self.assertIs(1+1, 2)


class ViewTests(TestCase):
    client = Client()

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEquals(response.status_code, 302)
