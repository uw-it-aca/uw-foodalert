import os
import json
from django.test import TestCase, Client
from django.db import connection
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

import foodalert
from foodalert.models import *
from foodalert.serializers import *
from foodalert.views import NotificationDetail, NotificationList


RESOURCE_DIR = os.path.join(os.path.dirname(foodalert.__file__),
                            'test',
                            'resources')


class NotificationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up a single mock user that can be used for all tests on
        notification tests
        """
        cls.user = User.objects.create_user(username='testuser',
                                            email="testuser@test.com",
                                            password="test")

    def setUp(self):
        # Set up a test notification with arbitrary field values
        notification = Notification.objects.create(
            location="UW Campus",
            event="UW Event",
            food_served="Food",
            amount_of_food_left="No Food",
            host=self.user,
            host_user_agent="browser")
        self.notification = notification

    def tearDown(self):
        Notification.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def test_get_notification_list(self):
        """
        Loads mock JSON response data for getting all notification and compares
        the expeced datato what is actually returned from get_notification
        """
        # Load expected_json mock resource to compare to the actual
        path = os.path.join(RESOURCE_DIR, 'notification_list.json')
        with open(path) as data_file:
            expected_json = json.load(data_file)
        client = Client()
        # Get all notifications from the notification endpoint
        response = client.get('/notification/')
        # Assert that the response is successful (200 HTTP Response Code)
        self.assertEqual(response.status_code, 200)
        # Convert response to JSON
        actual_json = response.json()
        # Set the created time to match as this field is dynamic/based on time
        expected_json[0]["id"] = actual_json[0]["id"]
        expected_json[0]["time"]["created"] = actual_json[0]["time"]["created"]
        # Assert that the content is a list with a single notification entry
        self.assertEqual(len(actual_json), 1)
        # Assert that the json of the notification is correct to the expected
        self.assertEqual(expected_json[0], actual_json[0])

    def test_get_notification_detail_by_id(self):
        """
        Loads mock JSON response data for getting a single notification
        and compares the expected data to the response data
        """
        # Load mock JSON for a single notification detail
        path = os.path.join(RESOURCE_DIR, 'notification_detail.json')
        with open(path) as data_file:
            expected_json = json.load(data_file)
        client = Client()
        # Get a single notification by ID
        url = '/notification/' + str(self.notification.id) + '/'
        response = client.get(url)
        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)
        # Convert response to JSON as the actual json
        actual_json = response.json()
        # Set the created time to match as this field is dynamic/based on time
        expected_json["id"] = actual_json["id"]
        expected_json["time"]["created"] = actual_json["time"]["created"]
        self.assertEqual(expected_json, actual_json)

    def test_post_valid_notification(self):
        """
        Attempts to post a valid notification payload and tests that the
        request is successful and the response json is matches the request data
        """
        # Load mock JSON for a typical notification post response
        path = os.path.join(RESOURCE_DIR, 'notification_post_response.json')
        with open(path) as data_file:
            expected_json = json.load(data_file)
        # Test the post with a valid payload (all fields necessary are there)
        valid_payload = {
                "location": {
                    "main": "UW Campus",
                    "detail": "North Campus"
                },
                "event": "UW Event",
                "time": {
                    "created": "2018-09-13T19:25:40.440859Z",
                    "ended": "2018-09-13T19:23:06.508534Z"
                },
                "food": {
                    "served": "Food",
                    "amount": "No Food",
                    "allergens": None
                },
                "bringContainers": False,
                "foodServiceInfo": {
                    "permitNumber": "12345",
                    "safeToShareFood": None
                },
                "host": {
                    "userAgent": "browser"
                }
            }
        factory = APIRequestFactory()
        request = factory.post(
                "/notification/",
                valid_payload,
                format='json'
            )
        force_authenticate(request, user=self.user)
        response = NotificationList.as_view()(request)
        # Assert that the posted notificaiton was sucessfully created
        self.assertEqual(response.status_code, 201)
        # Convert the response to JSON as the actual json
        actual_json = response.data
        # Set the created time to match as this field is dynamic/based on time
        expected_json["id"] = actual_json["id"]
        expected_json["time"]["created"] = actual_json["time"]["created"]
        self.assertEqual(expected_json, actual_json)

    def test_post_invalid_notification(self):
        """
        Attempts to post an invalid notification payload and tests that the
        request is unsuccessful
        """
        invalid_payload = {
                 "location": {
                     "main": None,
                     "detail": None
                 },
                 "event": "",
                 "time": {
                     "created": None,
                     "ended": ""
                 },
                 "food": {
                     "served": "Food",
                     "amount": "No Food",
                     "allergens": None
                 },
                 "bringContainers": False,
                 "foodServiceInfo": {
                     "permitNumber": "",
                     "safeToShareFood": None
                 },
                 "host": {
                     "userAgent": "browser"
                 }
            }
        factory = APIRequestFactory()
        request = factory.post(
                "/notification/",
                invalid_payload,
                format='json'
            )
        force_authenticate(request, user=self.user)
        response = NotificationList.as_view()(request)

        self.assertEqual(response.status_code, 400)

    def test_post_incomplete_payload(self):
        """
        Attempts to post an incomplete payload that does not have the
        required fields
        """
        incomplete_payload = {}

        factory = APIRequestFactory()
        request = factory.post(
                "/notification/",
                incomplete_payload,
                format='json'
            )
        force_authenticate(request, user=self.user)
        response = NotificationList.as_view()(request)

        self.assertEqual(response.status_code, 400)
