import os
import json
from datetime import datetime, timedelta
from unittest.mock import patch

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
from foodalert.test.test_utils import create_notification_from_data,\
    generate_amazon_mock, generate_twilio_mock,\
    create_user_and_client_from_data

RESOURCE_DIR = os.path.join(os.path.dirname(foodalert.__file__),
                            'test',
                            'resources')

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']


class NotificationTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up a single mock user that can be used for all tests on
        notification tests
        """
        # Load test_data mock resource
        path = os.path.join(RESOURCE_DIR, 'notification_details.json')
        with open(path) as data_file:
            cls.test_data = json.load(data_file)

        for allergen in cls.test_data["allergens"]:
            Allergen.objects.create(name=allergen)

        (cls.user1, cls.client_1) = create_user_and_client_from_data(
            cls.test_data["users"][0],
            [create_group, audit_group]
        )
        (cls.user2, cls.client_2) = create_user_and_client_from_data(
            cls.test_data["users"][1],
            [create_group, audit_group]
        )
        (cls.user3, cls.client_3) = create_user_and_client_from_data(
            cls.test_data["users"][2],
            [create_group, audit_group]
        )
        (cls.user4, cls.client_4) = create_user_and_client_from_data(
            cls.test_data["users"][3],
            [audit_group]
        )
        (cls.user5, cls.client_5) = create_user_and_client_from_data(
            cls.test_data["users"][4],
            [create_group]
        )
        (cls.user6, cls.client_6) = create_user_and_client_from_data(
            cls.test_data["users"][5],
            []
        )

        Subscription.objects.create(
            user=cls.user1, email=cls.test_data["subscription"]["email"],
            email_verified=cls.test_data["subscription"]["email_verified"],
            sms_number=cls.test_data["subscription"]["sms_number"],
            number_verified=cls.test_data["subscription"]["number_verified"],
            notif_on=cls.test_data["subscription"]["notif_on"]
        )

        cls.test_data = cls.test_data["notifications"]

        create_notification_from_data(cls.test_data[0], cls.user1)
        create_notification_from_data(cls.test_data[1], cls.user2)

        cls.test_data[2]["host"] = cls.user3

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Notification.objects.all().delete()

    """
    GET tests
    """
    def test_get_notification_list(self):
        """
        Compares the test data to what is actually returned from GET
        """
        # Get all notifications from the notification endpoint
        response = self.client_3.get('/notification/')
        # Assert that the response is successful (200 HTTP Response Code)
        self.assertEqual(response.status_code, 200)

        # Assert that the json of the notification is correct
        self.assertEqual(len(response.json()), 2)
        actual_json = json.dumps(response.json())

        expected_reponse_json = json.dumps([self.data_to_list_represent(data)
                                            for data in self.test_data[:2]])
        self.assertEqual(expected_reponse_json, actual_json)

    def test_get_notification_list_with_host_netid(self):
        """
        Compares the test data to what is actually returned from GET with
        host_netid
        """
        # Get all notifications from the notification endpoint
        response = self.client_3.get('/notification/?host_netid=' +
                                     self.user1.username)
        # Assert that the response is successful (200 HTTP Response Code)
        self.assertEqual(response.status_code, 200)

        # Assert that the json of the notification is correct
        self.assertEqual(len(response.json()), 1)
        actual_json = response.json()

        expected_reponse_json = [self.data_to_list_represent(
            self.test_data[0]
        )]
        self.assertEqual(expected_reponse_json, actual_json)

    def test_get_notification_detail_by_id(self):
        """
        Compares the test data to what is actually returned from GET
        at an id endpoint
        """
        # Get a single notification by ID
        url = '/notification/' + str(self.test_data[0]["id"]) + '/'
        response = self.client_3.get(url)
        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)
        actual_json1 = json.dumps(response.json())

        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[0]),
                         actual_json1)

        url = '/notification/' + str(self.test_data[1]["id"]) + '/'
        response = self.client_3.get(url)
        # Assert that the response is successful
        self.assertEqual(response.status_code, 200)
        actual_json2 = json.dumps(response.json())

        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[1]),
                         actual_json2)

        # Assert that the two responses were not equal
        self.assertNotEqual(actual_json1, actual_json2)

    """def test_perm_list_get(self):
        response = self.client_4.get('/notification/')
        self.assertEqual(response.status_code, 200)

        response = self.client_5.get('/notification/')
        self.assertEqual(response.status_code, 200)

        response = self.client_6.get('/notification/')
        self.assertEqual(response.status_code, 403)

    def test_perm_detail_get(self):
        url = '/notification/' + str(self.test_data[0]["id"]) + '/'

        response = self.client_4.get(url)
        self.assertEqual(response.status_code, 200)

        # client 5 has not created this notification
        response = self.client_5.get(url)
        self.assertEqual(response.status_code, 403)

        response = self.client_6.get(url)
        self.assertEqual(response.status_code, 403)"""

    """
    POST tests
    """
    def test_post_valid_notification(self):
        """
        Attempts to post a valid notification payload and tests that the
        request is successful and the response json is matches the request
        data
        """
        with generate_twilio_mock() as mock:
            end_time = datetime.now().astimezone() + timedelta(seconds=3600)
            response = self.client_3.post(
                    "/notification/",
                    data=self.data_to_payload_json(self.test_data[2],
                                                   end_time.isoformat()),
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
            self.test_data[2]["end_time"] = end_time
            expected_json = self.data_to_detail_json(self.test_data[2])
            self.assertEqual(expected_json, actual_json)

            url = '/notification/' + str(self.test_data[2]["id"]) + '/'
            response = self.client_3.get(url)
            # Assert that the response is successful
            self.assertEqual(response.status_code, 200)
            actual_json = json.dumps(response.json())
            self.assertEqual(expected_json, actual_json)

            # Get all notifications from the notification endpoint
            response = self.client_3.get('/notification/')
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
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        temp_location = self.test_data[2]["location"]
        self.test_data[2]["location"] = None
        invalid_payload = self.data_to_payload_json(self.test_data[2],
                                                    end_time)
        self.test_data[2]["location"] = temp_location

        response = self.client_3.post(
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
        end_time = datetime.now().astimezone() + timedelta(seconds=3600)
        invalid_payload = self.data_to_payload_json(
            self.test_data[2],
            end_time.isoformat()
        )

        with generate_twilio_mock() as mock:
            response = self.client_1.post(
                    "/notification/",
                    data=invalid_payload,
                    content_type='application/json'
                )
            self.assertEqual(response.status_code, 409)
            self.assertEqual(json.dumps(
                {"Conflict": "event with this netId is already in progress"}),
                json.dumps(response.json()))

            self.test_data[3]["host"] = self.user2
            valid_payload = self.data_to_payload_json(
                self.test_data[3],
                end_time.isoformat()
            )

            response = self.client_2.post(
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
            self.test_data[3]["end_time"] = end_time

            expected_json = self.data_to_detail_json(self.test_data[3])
            self.assertEqual(expected_json, actual_json)

    def test_post_incomplete_payload(self):
        """
        Attempts to post an incomplete payload that does not have the
        required fields
        """
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        proper_payload = \
            json.loads(self.data_to_payload_json(self.test_data[3], end_time))
        incomplete_payload = {}

        response = self.client_3.post(
                "/notification/",
                data=json.dumps(incomplete_payload),
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 400)

        with patch.multiple(settings, FOODALERT_USE_SMS="amazon"):
            with generate_amazon_mock() as mock:
                for key in proper_payload:
                    incomplete_payload[key] = proper_payload[key]
                    response = self.client_3.post(
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
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        self.test_data[3]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[3], end_time)

        response = self.client_3.post(
                "/notification/0/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

        response = self.client_3.post(
                "/notification/5/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    """def test_perm_list_post(self):
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        proper_payload = \
            json.loads(self.data_to_payload_json(self.test_data[3], end_time))

        with generate_twilio_mock() as mock:
            response = self.client_4.post(
                '/notification/',
                data=proper_payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 403)

            response = self.client_5.post(
                '/notification/',
                data=proper_payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)

            response = self.client_6.post(
                '/notification/',
                data=proper_payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 403)"""

    """
    PATCH tests
    """
    def test_patch_notification(self):
        """
        Attempts to patch a notification expect a 405
        """
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        self.test_data[3]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[3], end_time)
        response = self.client_3.patch(
                "/notification/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    def test_patch_notification_id(self):
        """
        Attempts to patch a notification at id expect a 405
        """
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        self.test_data[3]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[3], end_time)
        response = self.client_3.patch(
                "/notification/0/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

        valid_payload = self.data_to_payload_json(self.test_data[3], end_time)
        response = self.client_3.patch(
                "/notification/5/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    """
    DELETE tests
    """
    def test_delete_notification(self):
        """
        Attempts to patch a notification expect a 405
        """
        response = self.client_3.delete(
                "/notification/",
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    def test_delete_notification_id(self):
        """
        Attempts to patch a notification at id expect a 405
        """
        response = self.client_1.delete(
                "/notification/0/",
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

        response = self.client_3.delete(
                "/notification/5/",
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 405)

    """
    Helper functions
    """
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

    def data_to_payload_json(self, data, end):
        return json.dumps(
            {
                "netID": data["host"].username,
                "location": data["location"],
                "event": data["event"],
                "end_time": end,
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
