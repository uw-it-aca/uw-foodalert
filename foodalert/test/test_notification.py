import os
import json
from datetime import datetime, timedelta
from django.test import TestCase, Client
from django.db import connection
from django.conf import settings
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.test import APIRequestFactory, force_authenticate

import foodalert
from foodalert.models import Notification, Allergen, Subscription
from foodalert.serializers import NotificationDetailSerializer
from foodalert.views import NotificationDetail, NotificationList
from foodalert.sender import TwilioSender, Sender, AmazonSNSProvider
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

        for allergen in cls.test_data["allergens"]:
            Allergen.objects.create(name=allergen)

        Subscription.objects.create(
            user=cls.user1, email=cls.test_data["subscription"]["email"],
            email_verified=cls.test_data["subscription"]["email_verified"],
            sms_number=cls.test_data["subscription"]["sms_number"],
            number_verified=cls.test_data["subscription"]["number_verified"],
            notif_on=cls.test_data["subscription"]["notif_on"]
        )

        cls.test_data = cls.test_data["notifications"]

        cls.create_notification_from_data(0, cls.user1)
        cls.create_notification_from_data(1, cls.user2)

    def setUp(self):
        # Set up a test notification with arbitrary field values
        self.client = Client()
        self.client.force_login(self.user3)
        self.test_data[2]["host"] = self.user3

    def tearDown(self):
        Notification.objects.all().delete()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    """
    GET testes
    """
    def test_get_notification_list(self):
        """
        Compares the test data to what is actually returned from GET
        """
        # Get all notifications from the notification endpoint
        response = self.client.get('/notification/')
        # Assert that the response is successful (200 HTTP Response Code)
        self.assertEqual(response.status_code, 200)

        # Assert that the json of the notification is correct
        self.assertEqual(len(response.json()), 2)
        actual_json = json.dumps(response.json())

        expected_reponse_json = json.dumps([self.data_to_list_represent(data)
                                            for data in self.test_data[:2]])
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
        actual_json1 = json.dumps(response.json())

        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[0]),
                         actual_json1)

        url = '/notification/' + str(self.test_data[1]["id"]) + '/'
        response = self.client.get(url)
        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)
        actual_json2 = json.dumps(response.json())

        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[1]),
                         actual_json2)

        # Assert that the two responses were not equal
        self.assertNotEqual(actual_json1, actual_json2)

    """
    POST testes
    """
    def test_post_valid_notification(self):
        """
        Attempts to post a valid notification payload and tests that the
        request is successful and the response json is matches the request
        data
        """
        with self.generate_twilio_mock() as mock:
            response = self.client.post(
                    "/notification/",
                    data=self.data_to_payload_json(self.test_data[2], 3600),
                    content_type='application/json'
                )

            # Assert that the posted notificaiton was sucessfully created
            self.assertEqual(response.status_code, 201)
            # Convert the response to JSON as the actual json
            actual_json = json.dumps(response.json())
            # Set the created time to match: this field is dynamic
            self.test_data[2]["id"] = response.data["id"]
            self.test_data[2]["created_time"] = \
                response.data["time"]["created"]
            self.test_data[2]["end_time"] = response.data["time"]["created"] \
                + timedelta(seconds=3600)
            temp_ms = response.data["time"]["end"]
            self.test_data[2]["end_time"] = self.test_data[2]["end_time"]\
                .replace(microsecond=temp_ms.microsecond)
            expected_json = self.data_to_detail_json(self.test_data[2])
            self.assertEqual(expected_json, actual_json)

            url = '/notification/' + str(self.test_data[2]["id"]) + '/'
            response = self.client.get(url)
            # Assert that the response is successful
            self.assertEqual(response.status_code, 200)
            actual_json = json.dumps(response.json())
            self.assertEqual(expected_json, actual_json)

            # Get all notifications from the notification endpoint
            response = self.client.get('/notification/')
            # Assert that the response is successful (200 HTTP Response Code)
            self.assertEqual(response.status_code, 200)
            actual_json = response.json()

            # Assert that the json of the notification is correct
            self.assertEqual(len(actual_json), 3)

            expected_reponse_json = json.dumps([
                self.data_to_list_represent(data)
                for data in self.test_data[:3]])
            self.assertEqual(expected_reponse_json, json.dumps(actual_json))

    def test_post_malformed_notification(self):
        """
        Attempts to post an malformed notification payload and tests that the
        request is unsuccessful
        """
        temp_location = self.test_data[2]["location"]
        self.test_data[2]["location"] = None
        invalid_payload = self.data_to_payload_json(self.test_data[2], 3600)
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
        invalid_payload = self.data_to_payload_json(self.test_data[2], 3600)

        with self.generate_twilio_mock() as mock:
            temp_client = Client()
            temp_client.force_login(self.user1)
            response = temp_client.post(
                    "/notification/",
                    data=invalid_payload,
                    content_type='application/json'
                )
            self.assertEqual(response.status_code, 409)
            self.assertEqual(json.dumps(
                {"Conflict": "event with this netId is already in progress"}),
                json.dumps(response.json()))

            self.test_data[3]["host"] = self.user2
            valid_payload = self.data_to_payload_json(self.test_data[3], 3600)

            temp_client = Client()
            temp_client.force_login(self.user2)
            response = temp_client.post(
                    "/notification/",
                    data=valid_payload,
                    content_type='application/json'
                )
            self.assertEqual(response.status_code, 201)
            # Convert the response to JSON as the actual json
            actual_json = json.dumps(response.json())
            # Set the created time to match: this field is dynamic
            self.test_data[3]["id"] = response.data["id"]
            self.test_data[3]["created_time"] = \
                response.data["time"]["created"]
            self.test_data[3]["end_time"] = \
                response.data["time"]["created"] + timedelta(seconds=3600)
            temp_ms = response.data["time"]["end"]
            self.test_data[3]["end_time"] = self.test_data[3]["end_time"]\
                .replace(microsecond=temp_ms.microsecond)

            expected_json = self.data_to_detail_json(self.test_data[3])
            self.assertEqual(expected_json, actual_json)

    def test_post_incomplete_payload(self):
        """
        Attempts to post an incomplete payload that does not have the
        required fields
        """
        proper_payload = \
            json.loads(self.data_to_payload_json(self.test_data[3], 3600))
        incomplete_payload = {}

        response = self.client.post(
                "/notification/",
                data=json.dumps(incomplete_payload),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)

        with patch.object(settings, 'FOODALERT_USE_SMS',
                          return_value="amazon"):
            with self.generate_amazon_mock() as mock:
                for key in proper_payload:
                    incomplete_payload[key] = proper_payload[key]
                    response = self.client.post(
                        "/notification/",
                        data=json.dumps(incomplete_payload),
                        content_type='application/json'
                    )
                    if incomplete_payload != proper_payload:
                        self.assertEqual(response.status_code, 400)
                    else:
                        self.assertEqual(response.status_code, 201)

    def test_post_to_id(self):
        """
        Attempts to post to 1 valid ID and 1 invalid ID and expects 405
        """
        self.test_data[3]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[3], 3600)

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

    """
    PATCH testes
    """
    def test_patch_notification(self):
        """
        Attempts to patch a notification expect a 405
        """
        self.test_data[3]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[3], 3600)
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
        valid_payload = self.data_to_payload_json(self.test_data[3], 3600)
        response = self.client.patch(
                "/notification/0/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

        valid_payload = self.data_to_payload_json(self.test_data[3], 3600)
        response = self.client.patch(
                "/notification/5/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    """
    DELETE testes
    """
    def test_delete_notification(self):
        """
        Attempts to patch a notification expect a 405
        """
        response = self.client.delete(
                "/notification/",
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    def test_delete_notification_id(self):
        """
        Attempts to patch a notification at id expect a 405
        """
        response = self.client.delete(
                "/notification/0/",
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(
                "/notification/5/",
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    @classmethod
    def create_notification_from_data(cls, index, user):
        notif_obj = Notification.objects.create(
            location=cls.test_data[index]["location"],
            event=cls.test_data[index]["event"],
            end_time=datetime.strptime(cls.test_data[index]["end_time"]
                                       + "+0000", "%Y-%m-%dT%H:%M:%S.%fZ%z"),
            food_served=cls.test_data[index]["food_served"],
            amount_of_food_left=cls.test_data[index]["amount_of_food_left"],
            bring_container=cls.test_data[index]["bring_container"],
            host=user,
            host_user_agent=cls.test_data[index]["userAgent"],
            ended=cls.test_data[index]["ended"])
        for allergen in cls.test_data[index]["allergens"]:
            notif_obj.allergens.add(Allergen.objects.get(name=allergen))
        cls.test_data[index]["id"] = notif_obj.id
        cls.test_data[index]["created_time"] = notif_obj.created_time
        cls.test_data[index]["end_time"] = notif_obj.end_time
        cls.test_data[index]["host"] = user

    def data_to_list_represent(self, data):
        return {
                "id": data["id"],
                "netID": data["host"].username,
                "event": data["event"],
                "ended": data["ended"]
            }

    def data_to_detail_json(self, data):
        return json.dumps(
            {
                "id": data["id"],
                "netID": data["host"].username,
                "location": data["location"],
                "event": data["event"],
                "time": {
                    "created": data["created_time"]
                    .strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
                    "end": data["end_time"].strftime("%Y-%m-%dT%H:%M:%S.%fZ")
                },
                "bring_container": data["bring_container"],
                "food": {
                    "served": data["food_served"],
                    "amount": data["amount_of_food_left"],
                    "allergens": data["allergens"]
                },
                "userAgent": data["userAgent"],
                "ended": data["ended"]
            },
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
                    "served": data["food_served"],
                    "amount": data["amount_of_food_left"],
                    "allergens": data["allergens"]
                },
                "host": {
                    "userAgent": data["userAgent"]
                }
            }
        )

    def generate_twilio_mock(self):
        ret = Mock()
        ret.body = ''
        ret.status = 200
        m2 = Mock()
        m2.notifications = Mock()
        m2.notifications.create = PropertyMock(return_value=ret)

        m1 = Mock()
        m1.notify = Mock()
        m1.notify.services = PropertyMock(return_value=m2)

        return patch.object(TwilioSender, 'c',
                            new_callable=PropertyMock, return_value=m1)

    def generate_amazon_mock(self):
        ret = {
            'failed': [],
            'successful': ['test']
        }
        return patch.object(AmazonSNSProvider, 'send_message',
                            return_value=ret)
