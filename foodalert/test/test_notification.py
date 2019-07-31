import os
import json
from datetime import timedelta
from django.test import TestCase, Client
from django.db import connection
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.test import APIRequestFactory, force_authenticate

import foodalert
from foodalert.models import Notification, Allergen
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
        cls.user1 = User.objects.create_user(username="testuser_one",
                                            email="testuser_one@test.com",
                                            password="test")
        cls.user2 = User.objects.create_user(username="testuser_two",
                                            email="testuser_two@test.com",
                                            password="test")
        cls.user3 = User.objects.create_user(username="testuser_three",
                                            email="testuser_three@test.com",
                                            password="test")
        # Load test_data mock resource
        path = os.path.join(RESOURCE_DIR, 'notification_details.json')
        with open(path) as data_file:
            cls.test_data = json.load(data_file)

    def setUp(self):
        # Set up a test notification with arbitrary field values
        self.create_notification_from_data(0, self.user1)
        self.create_notification_from_data(1, self.user2)
        self.client = Client()
        self.client.force_login(self.user3)
        self.test_data[2]["host"] = self.user3

    def tearDown(self):
        Notification.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def test_get_notification_list(self):
        """
        Compares the test data to what is actually returned from GET
        """
        # Get all notifications from the notification endpoint
        response = self.client.get('/notification/')
        # Assert that the response is successful (200 HTTP Response Code)
        self.assertEqual(response.status_code, 200)
        actual_json = response.json()
        
        # Assert that the json of the notification is correct
        self.assertEqual(len(actual_json), 2)
        expected_reponse_json = [self.data_to_list_json(data) for data in self.test_data[:2]]
        self.assertEqual(expected_reponse_json, actual_json)

    def test_get_notification_detail_by_id(self):
        """
        Compares the test data to what is actually returned from GET
        at an id endpoint
        """
        # Get a single notification by ID
        url = '/notification/' + str(self.test_data[0]["id"]) + '/'
        response = self.client.get(url)
        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)
        actual_json1 = response.json()

        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[0]), actual_json1)

        url = '/notification/' + str(self.test_data[1]["id"]) + '/'
        response = self.client.get(url)
        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)
        actual_json2 = response.json()

        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[1]), actual_json2)

        # Assert that the two responses were not equal
        self.assertNotEqual(actual_json1, actual_json2)

    def test_post_valid_notification(self):
        """
        Attempts to post a valid notification payload and tests that the
        request is successful and the response json is matches the request data
        """
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
                         TwilioSender, 'c',
                         new_callable=PropertyMock) as mock:
            mock.return_value = m1

            response = self.client.post(
                    "/notification/",
                    data=self.data_to_payload_json(self.test_data[2], 3600000),
                    content_type='application/json'
                )

            # Assert that the posted notificaiton was sucessfully created
            self.assertEqual(response.status_code, 201)
            # Convert the response to JSON as the actual json
            actual_json = response.data
            # Set the created time to match: this field is dynamic
            self.test_data[2]["id"] = response.data["id"]
            self.test_data[2]["created_time"] = response.data["time"]["created"]
            self.test_data[2]["end_time"] = response.data["time"]["created"] + timedelta(hours=1)
            expected_json = self.data_to_detail_json(self.test_data[2])
            
            self.assertEqual(expected_json, actual_json)

            url = '/notification/' + str(self.test_data[2]["id"]) + '/'
            response = self.client.get(url)
            # Assert that the response is successful
            self.assertEqual(response.status_code, 200)
            actual_json = response.json()

            self.assertEqual(expected_json, actual_json)

            # Get all notifications from the notification endpoint
            response = self.client.get('/notification/')
            # Assert that the response is successful (200 HTTP Response Code)
            self.assertEqual(response.status_code, 200)
            actual_json = response.json()
            
            # Assert that the json of the notification is correct
            self.assertEqual(len(actual_json), 3)

            expected_reponse_json = [self.data_to_list_json(data) for data in self.test_data[:3]]
            self.assertEqual(expected_reponse_json, actual_json)

    def test_post_malformed_notification(self):
        """
        Attempts to post an malformed notification payload and tests that the
        request is unsuccessful
        """
        temp_location = self.test_data[2]["location"]
        self.test_data[2]["location"] = None
        invalid_payload = self.data_to_payload_json(self.test_data[2], 3600000)
        self.test_data[2]["location"] = temp_location

        response = self.client.post(
                "/notification/",
                data=invalid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)

    def test_post_check_already_exist_notification(self):
        """
        First sends a payload for a user that already has an notification
        that has not ended. Then sends a payload for a user that already
        has an notification that has ended. The first one should cause an
        error 409 and the second one should return with a 201
        """
        invalid_payload = self.data_to_payload_json(self.test_data[2], 3600000)

        response = self.client.post(
                "/notification/",
                data=invalid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 409)
        self.assertEqual(json.loads(
            {"error": "event with this netId is already in progress"}),
            json.loads(response.data))
        
        self.test_data[3]["host"] = self.user2
        valid_payload = data_to_payload_json(self.test_data[3], 3600000)

        response = self.client.post(
                "/notification/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 201)
        # Convert the response to JSON as the actual json
        actual_json = response.data
        # Set the created time to match: this field is dynamic
        self.test_data[2]["id"] = response.data["id"]
        self.test_data[2]["created_time"] = response.data["time"]["created"]
        self.test_data[2]["end_time"] = response.data["time"]["created"] + timedelta(hours=1)

        expected_json = self.data_to_detail_json(self.test_data[2])
        self.assertEqual(expected_json, actual_json)

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

    def test_post_to_id(self):
        """
        Attempts to post to 1 valid ID and 1 invalid ID and expects 405
        """
        self.test_data[3]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[3], 3600000)

        response = self.client.post(
                "/notification/0/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

        response = self.client.post(
                "/notification/5/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    def test_patch_notification(self):
        """
        Attempts to patch a notification expect a 405
        """
        self.test_data[3]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[3], 3600000)
        response = self.client.patch(
                "/notification/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)
    
    def test_patch_notification_id(self):
        """
        Attempts to patch a notification at id expect a 405
        """
        self.test_data[3]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[3], 3600000)
        response = self.client.patch(
                "/notification/0/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

        valid_payload = self.data_to_payload_json(self.test_data[3], 3600000)
        response = self.client.patch(
                "/notification/5/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)
    
    def create_notification_from_data(self, index, user):
        notif_obj = notification = Notification.objects.create(
            location=self.test_data[index]["location"],
            event=self.test_data[index]["event"],
            food_served=self.test_data[index]["food_served"],
            amount_of_food_left=self.test_data[index]["amount_of_food_left"],
            bring_container=self.test_data[index]["bring_container"],
            host=user,
            host_user_agent=self.test_data[index]["userAgent"])
        for allergen in self.test_data[index]["allergens"]:
            notif_obj.allergens.add(Allergen.objects.get(name=allergen))
        self.test_data[index]["id"] = notif_obj.id
        self.test_data[index]["created_time"] = notif_obj.created_time
        self.test_data[index]["host"] = user

    def data_to_list_json(self, data):
        return json.dumps(
            {
                "id": data["id"],
                "netID": data["host"].username,
                "event": data["event"],
                "ended": data["ended"]
            },
            cls=DjangoJSONEncoder
        )
    
    def data_to_detail_json(self, data):
        return json.dumps(
            {
                "id": data["id"],
                "netID": data["host"].username,
                "location": data["location"],
                "event": data["event"],
                "time": {
                    "created_time": data["created_time"],
                    "end_time": data["end_time"]
                },
                "bring_container": data["bring_container"],
                "food": {
                    "food_served": data["food_served"],
                    "amount_of_food_left": data["amount_of_food_left"],
                    "allergens": data["allergens"]
                },
                "ended": data["ended"]
            },
            cls=DjangoJSONEncoder
        )
    
    def data_to_payload_json(self, data, duration):
        return json.dumps(
            {
                "netID": data["host"].username,
                "location": data["location"],
                "event": data["event"],
                "duration": duration,
                "bring_container": data["bring_container"],
                "food": {
                    "food_served": data["food_served"],
                    "amount_of_food_left": data["amount_of_food_left"],
                    "allergens": data["allergens"]
                },
                "host": {
                    "userAgent": data["userAgent"]
                }
            },
            cls=DjangoJSONEncoder
        )
