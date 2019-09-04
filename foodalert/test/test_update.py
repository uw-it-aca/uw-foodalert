from copy import deepcopy
from datetime import datetime
import json
import os
from unittest.mock import patch, Mock, PropertyMock

from django.test import TestCase, Client
from django.db.utils import IntegrityError
from django.conf import settings
from django.contrib.auth.models import User

import foodalert
from foodalert.models import Update, Notification, Allergen, FoodQualification
from foodalert.views import UpdateDetail, UpdateList
from foodalert.sender import TwilioSender
from foodalert.test.test_utils import create_notification_from_data, \
    create_update_from_data, generate_twilio_mock,\
    create_user_from_data, create_client_with_mock_saml

"""
May need to add model tests if the model is complecated

Stuff to test:
Real endpoints

GET /updates/
    - Test the format is right when multiple updates are listed. - X
GET /updates/?parent_notification_id=<integer>
    - Test the format is right when multiple updates are listed. - X
    - Test that only the relevent updates are listed - X
    - Test that only children of notificatons created by the user are
      accessible - X
GET /updates/<id>/
    - Test that the right json is returned - X
    - Test the case when the element with that id does not exist - X
POST /updates/
    - Test if this action creates an update. - X
    - Test an update request with fields missing. - X
    - Test that a update with ended: true ends and notification - X
    - Test that an update with ended: false dosen't affect the notification - X
    - Test that no more updates can be created under an ended notificaitons - X
    - Test that ended: true always creates the same message. - TODO:: TBD
    - Test that a user can not create a update under a diffrent users
      notification. - X

405 endpoints

POST /updates/<id>
PUT /updates/
PUT /updates/<id>
PATCH /updates/
PATCH /updates/<id>
DELETE /updates/
DELETE /updates/<id>
"""

RESOURCE_DIR = os.path.join(os.path.dirname(foodalert.__file__),
                            'test',
                            'resources')

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']


class UpdateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up a mock user for testing API calls
        to the update endpoint
        """
        # Load test_data mock resource
        path = os.path.join(RESOURCE_DIR, 'update_details.json')
        with open(path) as data_file:
            cls.real_data = json.load(data_file)

        cls.user1 = create_user_from_data(cls.real_data["users"][0])
        cls.user2 = create_user_from_data(cls.real_data["users"][1])
        cls.user3 = create_user_from_data(cls.real_data["users"][2])

        for allergen in cls.real_data["allergens"]:
            Allergen.objects.create(name=allergen)
        
        for food_qualification in cls.real_data["food_qualifications"]:
            FoodQualification.objects.create(
                internalName=food_qualification["internalName"],
                externalName=food_qualification["externalName"]
            )

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Notification.objects.all().delete()
        Update.objects.all().delete()
        Allergen.objects.all().delete()
        FoodQualification.objects.all().delete()

    def setUp(self):
        self.test_data = deepcopy(self.real_data)
        create_notification_from_data(
            self.test_data["notifications"][0],
            self.user1
        )
        create_notification_from_data(
            self.test_data["notifications"][1],
            self.user2
        )

        create_update_from_data(
            self.test_data["updates"][0],
            self.test_data["notifications"]
        )
        create_update_from_data(
            self.test_data["updates"][1],
            self.test_data["notifications"]
        )
        create_update_from_data(
            self.test_data["updates"][3],
            self.test_data["notifications"]
        )

    def test_get_update_list(self):
        """
        Compares the test data to what is actually returned from GET
        """
        # Audit and create
        client = create_client_with_mock_saml(
            self.user1,
            [create_group, audit_group]
        )
        response = client.get('/updates/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 3)

        expected_reponse_json = \
            [self.data_to_list_represent(self.test_data["updates"][0]),
             self.data_to_list_represent(self.test_data["updates"][1]),
             self.data_to_list_represent(self.test_data["updates"][3])]
        self.assertEqual(expected_reponse_json, response.json())

        # Audit
        client = create_client_with_mock_saml(
            self.user1,
            [audit_group]
        )
        response = client.get('/updates/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 3)

        expected_reponse_json = \
            [self.data_to_list_represent(self.test_data["updates"][0]),
             self.data_to_list_represent(self.test_data["updates"][1]),
             self.data_to_list_represent(self.test_data["updates"][3])]
        self.assertEqual(expected_reponse_json, response.json())

        # Host
        client = create_client_with_mock_saml(
            self.user1,
            [create_group]
        )
        response = client.get('/updates/')
        self.assertEqual(response.status_code, 403)

        # []
        client = create_client_with_mock_saml(
            self.user1,
            []
        )
        response = client.get('/updates/')
        self.assertEqual(response.status_code, 403)

    def test_get_update_list_query_args(self):
        """
        Compares the test data to what is actually returned from GET with
        query params
        """
        # Audit
        client = create_client_with_mock_saml(
            self.user1,
            [audit_group]
        )
        response = client.get("/updates/?parent_notification={0}".format(
            self.test_data["notifications"][0]["id"]
        ))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 2)

        expected_reponse_json = \
            [self.data_to_list_represent(self.test_data["updates"][0]),
             self.data_to_list_represent(self.test_data["updates"][1])]
        self.assertEqual(expected_reponse_json, response.json())

        # Host - self
        client = create_client_with_mock_saml(
            self.user1,
            [create_group]
        )
        response = client.get("/updates/?parent_notification={0}".format(
            self.test_data["notifications"][0]["id"]
        ))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 2)

        expected_reponse_json = \
            [self.data_to_list_represent(self.test_data["updates"][0]),
             self.data_to_list_represent(self.test_data["updates"][1])]
        self.assertEqual(expected_reponse_json, response.json())

        # Host - other
        client = create_client_with_mock_saml(
            self.user2,
            [create_group]
        )
        response = client.get("/updates/?parent_notification={0}".format(
            self.test_data["notifications"][0]["id"]
        ))
        self.assertEqual(response.status_code, 403)

        # []
        client = create_client_with_mock_saml(
            self.user1,
            []
        )
        response = client.get("/updates/?parent_notification={0}".format(
            self.test_data["notifications"][0]["id"]
        ))
        self.assertEqual(response.status_code, 403)

    def test_get_update_detail_by_id(self):
        """
        Compares the test data to what is actually returned from GET
        at an id endpoint
        """
        # Audit
        client = create_client_with_mock_saml(
            self.user1,
            [audit_group]
        )
        response = client.get("/updates/{0}/".format(
            self.test_data["updates"][0]["id"]
        ))

        self.assertEqual(response.status_code, 200)

        expected_reponse_json = self.data_to_detail_represent(
            self.test_data["updates"][0],
            response.json()["created_time"]
        )
        self.assertEqual(expected_reponse_json, response.json())

        # Host - self
        client = create_client_with_mock_saml(
            self.user1,
            [create_group]
        )
        response = client.get("/updates/{0}/".format(
            self.test_data["updates"][0]["id"]
        ))

        self.assertEqual(response.status_code, 200)

        expected_reponse_json = self.data_to_detail_represent(
            self.test_data["updates"][0],
            response.json()["created_time"]
        )
        self.assertEqual(expected_reponse_json, response.json())

        # Host - other
        client = create_client_with_mock_saml(
            self.user2,
            [create_group]
        )
        response = client.get("/updates/{0}/".format(
            self.test_data["updates"][0]["id"]
        ))

        self.assertEqual(response.status_code, 403)

        # []
        client = create_client_with_mock_saml(
            self.user1,
            []
        )
        response = client.get("/updates/{0}/".format(
            self.test_data["updates"][0]["id"]
        ))

        self.assertEqual(response.status_code, 403)

    def test_get_update_detail_by_bad_id(self):
        """
        Compares the test data to what is actually returned from GET
        at an id endpoint
        """
        # Audit
        client = create_client_with_mock_saml(
            self.user1,
            [audit_group]
        )
        response = client.get("/updates/100/")

        self.assertEqual(response.status_code, 404)

    def test_post_valid_update(self):
        """
        Attempts to post a valid notification payload and tests that the
        request is successful and the response json is matches the request
        data
        """
        # Parent notification ID is 0
        payload = self.data_to_payload_represent(self.test_data["updates"][4])

        with generate_twilio_mock() as mock:
            # Audit
            client = create_client_with_mock_saml(
                self.user1,
                [audit_group]
            )
            response = client.post(
                "/updates/",
                payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 403)

            # Host - self
            client = create_client_with_mock_saml(
                self.user1,
                [create_group]
            )
            response = client.post(
                "/updates/",
                payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 201)

            self.test_data["updates"][4]["id"] = response.json()["id"]
            expected_reponse_json = self.data_to_detail_represent(
                self.test_data["updates"][4],
                response.json()["created_time"]
            )

            self.assertEqual(expected_reponse_json, response.json())

            response2 = client.get("/updates/{0}/".format(
                self.test_data["updates"][4]["id"]
            ))

            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response.json(), response2.json())

            # Host - other
            client = create_client_with_mock_saml(
                self.user2,
                [create_group]
            )
            response = client.post(
                "/updates/",
                payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 403)

            # []
            client = create_client_with_mock_saml(
                self.user1,
                []
            )
            response = client.post(
                "/updates/",
                payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 403)

    def test_post_malformed_update(self):
        """
        Attempts to post a malformed notification payload and tests that the
        request fails with error code 400
        """
        # Host - self
        client1 = create_client_with_mock_saml(
            self.user1,
            [create_group]
        )
        # Audit
        client2 = create_client_with_mock_saml(
            self.user2,
            [audit_group]
        )
        payload = self.data_to_payload_represent(self.test_data["updates"][5])

        response = client2.get('/updates/')
        self.assertEqual(response.status_code, 200)

        init_len = len(response.json())

        with generate_twilio_mock() as mock:
            response = client1.post("/updates/", {})
            self.assertEqual(response.status_code, 400)
            response = client2.get('/updates/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), init_len)

            invalid_payload = payload
            del invalid_payload["text"]

            response = client1.post("/updates/", invalid_payload)
            self.assertEqual(response.status_code, 400)
            response = client2.get('/updates/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), init_len)

            invalid_payload = payload
            del invalid_payload["parent_notification_id"]

            response = client1.post("/updates/", invalid_payload)
            self.assertEqual(response.status_code, 400)
            response = client2.get('/updates/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.json()), init_len)

    def test_post_ends_notif(self):
        """
        Attempts to post a valid notification payload and tests that the
        request is successful and the rparent notificaiton is ended
        """
        payload = self.data_to_payload_represent(self.test_data["updates"][6])

        self.assertIs(
            Notification.objects.get(
                pk=payload["parent_notification_id"]
            ).ended,
            False
        )

        with generate_twilio_mock() as mock:
            # Host - self
            client = create_client_with_mock_saml(
                self.user2,
                [create_group]
            )
            response = client.post(
                "/updates/",
                payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 201)

            self.assertIs(
                Notification.objects.get(
                    pk=payload["parent_notification_id"]
                ).ended,
                True
            )

            len_updates = len(Update.objects.all())
            payload = self.data_to_payload_represent(
                self.test_data["updates"][7]
            )
            response = client.post(
                "/updates/",
                payload,
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 400)

            self.assertIs(
                Notification.objects.get(
                    pk=payload["parent_notification_id"]
                ).ended,
                True
            )
            self.assertIs(len_updates, len(Update.objects.all()))

    def data_to_list_represent(self, data):
        parent_notification_id = \
            self.test_data["notifications"][
                data["parent_notification_id"]
            ]["id"]
        return {
            "id": data["id"],
            "parent_notification_id": parent_notification_id
        }

    def data_to_detail_represent(self, data, created_time):
        parent_notification_id = \
            self.test_data["notifications"][
                data["parent_notification_id"]
            ]["id"]
        return {
            "id": data["id"],
            "netID": Notification.objects.get(
                id=parent_notification_id
            ).host.username,
            "text": data["text"],
            "parent_notification_id": parent_notification_id,
            "created_time": created_time
        }

    def data_to_payload_represent(self, data):
        parent_notification_id = \
            self.test_data["notifications"][
                data["parent_notification_id"]
            ]["id"]
        payload = {
            "text": data["text"],
            "parent_notification_id": parent_notification_id
        }

        if "ended" in data:
            payload["ended"] = data["ended"]

        return payload
