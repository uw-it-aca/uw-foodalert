import json
from django.test import TestCase, Client
from django.contrib.auth.models import User

from foodalert.models import *
from foodalert.serializers import *

class NotificationTest(TestCase):

    def setUp(self):
        # Set up a test user for the notification host
        user = User.objects.create_user(username='testuser',
                                        email="testuser@test.com",
                                        password="test")
        # Set up a test notification with arbitrary field values
        notification = Notification.objects.create(location="UW Campus",
                                                   event="UW Event",
                                                   food_served="Food",
                                                   amount_of_food_left="No Food",
                                                   host = user,
                                                   host_user_agent="browser")
        self.notification = notification

    def tearDown(self):
        self.notification.delete()

    def test_get_notification_list(self):
        """
        Loads mock JSON response data for getting all notification and compares
        the expeced datato what is actually returned from get_notification
        """
        #Load expected_json mock resource to compare to the actual
        path = '/app/foodalert/test/resources/notification_list.json'
        with open(path) as data_file:
            expected_json = json.load(data_file)
        client = Client()
        # Get all notifications from the notification endpoint
        response = client.get('/notification/')
        # Assert that the response is successful (200 HTTP Response Code)
        self.assertEquals(response.status_code, 200)
        # Convert response to JSON
        actual_json = response.json()
        # Assert that the content is a list with a single notification entry
        self.assertEquals(len(actual_json), 1)
        # Assert that the json of the notification is correct to the expected
        self.assertEquals(actual_json[0]['location'], expected_json[0]['location'])

    def test_get_notification_detail_by_id(self):
        """
        Loads mock JSON response data for getting a single notification
        and compares the expected data to the response data
        """
        # Load mock JSON for a single notification detail
        path = '/app/foodalert/test/resources/notification_detail.json'
        with open(path) as data_file:
            expected_json = json.load(data_file)
        client = Client()
        # Get a single notification by ID
        url = '/notification/' + str(self.notification.id) + '/'
        response = client.get(url)
        # Assert that the response is successful
        self.assertEquals(response.status_code, 200)

        actual_json = response.json()
        self.assertEquals(actual_json['location'], expected_json['location'])

