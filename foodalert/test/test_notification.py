import os
import json
from django.test import TestCase, Client
from django.db import connection
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, force_authenticate

import foodalert
from foodalert.models import Notification
from foodalert.serializers import NotificationSerializer
from foodalert.views import NotificationDetail, NotificationList
from foodalert.sender import TwilioSender, Sender
from unittest.mock import patch, Mock, PropertyMock

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
        user = "testuser"
        passw = "test"
        cls.user = User.objects.create_user(username=user,
                                            email="testuser@test.com",
                                            password=passw,
                                            is_active=1)

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
        self.client = Client()
        self.client.force_login(self.user)

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
        # Get all notifications from the notification endpoint
        response = self.client.get('/notification/')
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
        # Get a single notification by ID
        url = '/notification/' + str(self.notification.id) + '/'
        response = self.client.get(url)
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
                "location": "UW Campus",
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
                    "safeToShareFood": None
                },
                "host": {
                    "userAgent": "browser"
                }
            }

        ret = Mock()
        ret.body = ''
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

            response = self.client.post(
                    "/notification/",
                    data=json.dumps(valid_payload),
                    content_type='application/json'
                )
            # Assert that the posted notificaiton was sucessfully created
            self.assertEqual(response.status_code, 201)
            # Convert the response to JSON as the actual json
            actual_json = response.data
            # Set the created time to match: this field is dynamic
            expected_json["id"] = actual_json["id"]
            expected_json["time"]["created"] = actual_json["time"]["created"]
            self.assertEqual(expected_json, actual_json)

    def test_post_invalid_notification(self):
        """
        Attempts to post an invalid notification payload and tests that the
        request is unsuccessful
        """
        invalid_payload = {
                 "location": None,
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
                     "safeToShareFood": None
                 },
                 "host": {
                     "userAgent": "browser"
                 }
            }

        response = self.client.post(
                "/notification/",
                data=json.dumps(invalid_payload),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)

    def test_post_incomplete_payload(self):
        """
        Attempts to post an incomplete payload that does not have the
        required fields
        """
        incomplete_payload = {}

        response = self.client.post(
                "/notification/",
                data=json.dumps(incomplete_payload),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)

    def test_patch_notification(self):
        """
        Attempts to patch a notification 'ended' field and tests that
        the parital update was successful
        """
        payload = {
            "ended": True
        }
        url = "/notification/" + str(self.notification.id) + "/"
        response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["ended"], True)

    def test_patch_notification_empty(self):
        """
        Attempts to patch a notification with an empty payload
        and tests that an error is raised
        """
        payload = {}
        url = "/notification/" + str(self.notification.id) + "/"
        response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b'{"Bad Request":"Patches only apply to the ended field"}')

    def test_patch_incorrect_fields(self):
        """
        Attempts to patch fields of a notification that are not the
        'ended' field and tests that an error is raised
        """
        payload = {
            "location": "Test",
            "ended": True
        }
        url = "/notification/" + str(self.notification.id) + "/"
        response = self.client.patch(
                url,
                data=json.dumps(payload),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.content,
            b'{"Bad Request":"Patches only apply to the ended field"}')
