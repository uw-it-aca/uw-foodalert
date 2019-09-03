import os
import json
from copy import deepcopy
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
    create_user_from_data, create_client_with_mock_saml

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
            cls.real_data = json.load(data_file)

        for allergen in cls.real_data["allergens"]:
            Allergen.objects.create(name=allergen)

        cls.user1 = create_user_from_data(cls.real_data["users"][0])
        cls.user2 = create_user_from_data(cls.real_data["users"][1])

        Subscription.objects.create(
            user=cls.user1, email=cls.real_data["subscription"]["email"],
            email_verified=cls.real_data["subscription"]["email_verified"],
            sms_number=cls.real_data["subscription"]["sms_number"],
            number_verified=cls.real_data["subscription"]["number_verified"],
            notif_on=cls.real_data["subscription"]["notif_on"]
        )

    def setUp(self):
        self.test_data = deepcopy(self.real_data["notifications"])
        create_notification_from_data(self.test_data[0], self.user1)
        create_notification_from_data(self.test_data[1], self.user2)

    def tearDown(self):
        Notification.objects.all().delete()
        self.test_data = []

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Notification.objects.all().delete()
        Allergen.objects.all().delete()

    """
    GET tests
    """
    def test_get_notification_list(self):
        """
        Compares the test data to what is actually returned from GET
        """
        client = create_client_with_mock_saml(
            self.user1,
            [create_group, audit_group]
        )
        response = client.get('/notification/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 2)

        self.assertEqual(
            response.json(),
            [self.data_to_list_represent(data) for data in self.test_data[:2]]
        )

        client = create_client_with_mock_saml(self.user1, [audit_group])
        response = client.get('/notification/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 2)

        self.assertEqual(
            response.json(),
            [self.data_to_list_represent(data) for data in self.test_data[:2]]
        )

        client = create_client_with_mock_saml(self.user1, [create_group])
        response = client.get('/notification/')
        self.assertEqual(response.status_code, 403)

        client = create_client_with_mock_saml(self.user1, [])
        response = client.get('/notification/')
        self.assertEqual(response.status_code, 403)

    def test_get_notification_list_with_host_netid(self):
        """
        Compares the test data to what is actually returned from GET with
        host_netid
        """
        # Audit
        client = create_client_with_mock_saml(
            self.user1,
            [audit_group]
        )
        response = client.get(
            "/notification/?host_netid={}".format(self.user1.username)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        expected_reponse_json = [self.data_to_list_represent(
            self.test_data[0]
        )]
        self.assertEqual(expected_reponse_json, response.json())

        # Host - self
        client = create_client_with_mock_saml(
            self.user1,
            [create_group]
        )
        response = client.get(
            "/notification/?host_netid={}".format(self.user1.username)
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        expected_reponse_json = [self.data_to_list_represent(
            self.test_data[0]
        )]
        self.assertEqual(expected_reponse_json, response.json())

        # Host - other
        client = create_client_with_mock_saml(
            self.user2,
            [create_group]
        )
        response = client.get(
            "/notification/?host_netid={}".format(self.user1.username)
        )
        self.assertEqual(response.status_code, 403)

        # []
        client = create_client_with_mock_saml(
            self.user1,
            []
        )
        response = client.get(
            "/notification/?host_netid={}".format(self.user1.username)
        )
        self.assertEqual(response.status_code, 403)

        # Bad netid
        Notification.objects.all().delete()
        client = create_client_with_mock_saml(
            self.user1,
            [audit_group]
        )
        response = client.get('/notification/?host_netid=neveruse')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 0)

    def test_get_notification_detail_by_id(self):
        """
        Compares the test data to what is actually returned from GET
        at an id endpoint
        """
        # Audit
        client = create_client_with_mock_saml(
            self.user1,
            [audit_group]
        )
        url = "/notification/{}/".format(str(self.test_data[0]["id"]))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[0]),
                         response.json())

        # Host - self - 1
        client = create_client_with_mock_saml(
            self.user1,
            [create_group]
        )
        url = "/notification/{}/".format(str(self.test_data[0]["id"]))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[0]),
                         response.json())

        # Host - self - 2
        client = create_client_with_mock_saml(
            self.user2,
            [create_group]
        )
        url = "/notification/{}/".format(str(self.test_data[1]["id"]))
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        # Assert that the json of the notification is correct
        self.assertEqual(self.data_to_detail_json(self.test_data[1]),
                         response.json())

        # Host - other
        client = create_client_with_mock_saml(
            self.user2,
            [create_group]
        )
        url = "/notification/{}/".format(str(self.test_data[0]["id"]))
        response = client.get(url)
        self.assertEqual(response.status_code, 403)

        # []
        client = create_client_with_mock_saml(
            self.user2,
            [create_group]
        )
        url = "/notification/{}/".format(str(self.test_data[0]["id"]))
        response = client.get(url)
        self.assertEqual(response.status_code, 403)

    """
    POST tests
    """
    def test_post_valid_notification(self):
        """
        Attempts to post a valid notification payload and tests that the
        request is successful and the response json is matches the request
        data
        """
        self.test_data[2]["host"] = self.user2

        with generate_twilio_mock() as mock:
            end_time = datetime.now().astimezone() + timedelta(seconds=3600)

            # Audit
            client = create_client_with_mock_saml(
                self.test_data[2]["host"],
                [audit_group]
            )
            response = client.post(
                "/notification/",
                data=self.data_to_payload_json(
                    self.test_data[2],
                    end_time.isoformat()
                ),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 403)

            # Host
            client = create_client_with_mock_saml(
                self.test_data[2]["host"],
                [create_group]
            )
            response1 = client.post(
                "/notification/",
                data=self.data_to_payload_json(
                    self.test_data[2],
                    end_time.isoformat()
                ),
                content_type='application/json'
            )
            self.assertEqual(response1.status_code, 201)
            self.test_data[2]["id"] = response1.data["id"]
            self.test_data[2]["created_time"] = \
                response1.data["time"]["created"]
            self.test_data[2]["end_time"] = end_time
            expected_json = self.data_to_detail_json(self.test_data[2])
            self.assertEqual(expected_json, response1.json())

            url = "/notification/{}/".format(str(self.test_data[2]["id"]))
            response2 = client.get(url)
            # Assert that the response is successful
            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response2.json(), response1.json())

            client = create_client_with_mock_saml(
                self.user1,
                [audit_group]
            )
            # Get all notifications from the notification endpoint
            response = client.get('/notification/')
            # Assert that the response is successful (200 HTTP Response Code)
            self.assertEqual(response.status_code, 200)
            actual_json = response.json()

            # Assert that the json of the notification is correct
            self.assertEqual(len(actual_json), 3)

            expected_reponse_json = json.dumps([
                self.data_to_list_represent(data)
                for data in self.test_data[:3]])
            self.assertEqual(expected_reponse_json, json.dumps(actual_json))

        self.test_data[2]["host"] = None

    def test_post_malformed_notification(self):
        """
        Attempts to post an malformed notification payload and tests that the
        request is unsuccessful
        """
        self.test_data[2]["host"] = self.user2
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        temp_location = self.test_data[2]["location"]
        self.test_data[2]["location"] = None
        invalid_payload = self.data_to_payload_json(self.test_data[2],
                                                    end_time)
        self.test_data[2]["location"] = temp_location

        client = create_client_with_mock_saml(
            self.test_data[2]["host"],
            [create_group]
        )
        response = client.post(
            "/notification/",
            data=invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.test_data[2]["host"] = None

    def test_post_check_already_exist_notification(self):
        """
        First sends a payload for a user that already has an notification
        that has not ended. Then sends a payload for a user that already
        has an notification that has ended. The first one should cause an
        error 409 and the second one should return with a 201
        """
        self.test_data[2]["host"] = self.user1
        self.test_data[3]["host"] = self.user2

        end_time = datetime.now().astimezone() + timedelta(seconds=3600)
        payload_data_2 = self.data_to_payload_json(
            self.test_data[2],
            end_time.isoformat()
        )
        payload_data_3 = self.data_to_payload_json(
            self.test_data[3],
            end_time.isoformat()
        )

        with generate_twilio_mock() as mock:
            client = create_client_with_mock_saml(
                self.test_data[2]["host"],
                [create_group]
            )
            response = client.post(
                "/notification/",
                data=payload_data_2,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 409)
            self.assertEqual(json.dumps(
                {"Conflict": "event with this netId is already in progress"}),
                json.dumps(response.json()))

            client = create_client_with_mock_saml(
                self.test_data[3]["host"],
                [create_group]
            )

            response = client.post(
                    "/notification/",
                    data=payload_data_3,
                    content_type='application/json'
                )
            self.assertEqual(response.status_code, 201)
            # Set the created time to match: this field is dynamic
            self.test_data[3]["id"] = response.data["id"]
            self.test_data[3]["created_time"] = \
                response.data["time"]["created"]
            self.test_data[3]["end_time"] = end_time
            self.assertEqual(
                self.data_to_detail_json(self.test_data[3]),
                response.json()
            )

        self.test_data[2]["host"] = None
        self.test_data[3]["host"] = None

    def test_post_incomplete_payload(self):
        """
        Attempts to post an incomplete payload that does not have the
        required fields
        """
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        self.test_data[2]["host"] = self.user2
        proper_payload = \
            json.loads(self.data_to_payload_json(self.test_data[2], end_time))
        incomplete_payload = {}

        client = create_client_with_mock_saml(
            self.test_data[2]["host"],
            [create_group]
        )
        response = client.post(
            "/notification/",
            data=json.dumps(incomplete_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        with patch.multiple(settings, FOODALERT_USE_SMS="amazon"):
            with generate_amazon_mock() as mock:
                for key in proper_payload:
                    incomplete_payload[key] = proper_payload[key]
                    response = client.post(
                        "/notification/",
                        data=json.dumps(incomplete_payload),
                        content_type='application/json'
                    )
                    if incomplete_payload != proper_payload:
                        self.assertEqual(response.status_code, 400)
                    else:
                        self.assertEqual(response.status_code, 201)

        self.test_data[2]["host"] = None

    def test_post_to_id(self):
        """
        Attempts to post to 1 valid ID and 1 invalid ID and expects 403
        """
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        self.test_data[2]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[2], end_time)

        client = create_client_with_mock_saml(
            self.test_data[2]["host"],
            [create_group, audit_group]
        )

        response = client.post(
            "/notification/1/",
            data=valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

        response = client.post(
            "/notification/5/",
            data=valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

        self.test_data[2]["host"] = None

    """
    PATCH tests
    """
    def test_patch_notification(self):
        """
        Attempts to patch a notification expect a 403
        """
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        self.test_data[2]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[2], end_time)

        client = create_client_with_mock_saml(
            self.test_data[2]["host"],
            [create_group, audit_group]
        )
        response = client.patch(
                "/notification/",
                data=valid_payload,
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 403)

        self.test_data[2]["host"] = None

    def test_patch_notification_id(self):
        """
        Attempts to patch a notification at id expect a 403
        """
        end_time = (datetime.now().astimezone() +
                    timedelta(seconds=3600)).isoformat()
        self.test_data[2]["host"] = self.user2
        valid_payload = self.data_to_payload_json(self.test_data[2], end_time)

        client = create_client_with_mock_saml(
            self.test_data[2]["host"],
            [create_group, audit_group]
        )
        response = client.patch(
            "/notification/1/",
            data=valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

        response = client.patch(
            "/notification/5/",
            data=valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

        self.test_data[2]["host"] = None

    """
    DELETE tests
    """
    def test_delete_notification(self):
        """
        Attempts to patch a notification expect a 403
        """
        client = create_client_with_mock_saml(
            self.user1,
            [create_group, audit_group]
        )
        response = client.delete(
            "/notification/",
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_notification_id(self):
        """
        Attempts to patch a notification at id expect a 403
        """
        client = create_client_with_mock_saml(
            self.user1,
            [create_group, audit_group]
        )
        response = client.delete(
                "/notification/1/",
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 403)

        response = client.delete(
                "/notification/5/",
                content_type='application/json'
            )
        self.assertEqual(response.status_code, 403)

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
        return {
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
            }

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
