from datetime import datetime
import json
import os
from unittest.mock import patch, Mock, PropertyMock

from django.test import TestCase, Client
from parameterized import parameterized, param
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

import foodalert
from foodalert.models import Update, Notification
from foodalert.views import UpdateDetail, UpdateList
from foodalert.sender import TwilioSender
from foodalert.test.test_utils import create_notification_from_data, \
    create_update_from_data, generate_twilio_mock

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
      accessible - TODO:: Need to add perm class
GET /updates/<id>/
    - Test that the right json is returned - X
    - Test the case when the element with that id does not exist - X
POST /updates/
    - Test if this action creates an update. - X
    - Test if multiple updates are created porperly
    - Test an update request with fields missing.
    - Test that a update with ended: true ends and notification
    - Test that an update with ended: false dosen't affect the notification
    - Test that no more updates can be created under an ended notificaitons
    - Test that ended: true always creates the same message.
    - Test that a user can not create a update under a diffrent users
      notification.

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


class UpdateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up a mock user for testing API calls
        to the update endpoint
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
        path = os.path.join(RESOURCE_DIR, 'update_details.json')
        with open(path) as data_file:
            cls.test_data = json.load(data_file)

        create_notification_from_data(cls.test_data["notifications"][0],
                                      cls.user1)
        create_notification_from_data(cls.test_data["notifications"][1],
                                      cls.user2)

        create_update_from_data(
            cls.test_data["updates"][0],
            cls.test_data["notifications"]
        )
        create_update_from_data(
            cls.test_data["updates"][1],
            cls.test_data["notifications"]
        )
        create_update_from_data(
            cls.test_data["updates"][3],
            cls.test_data["notifications"]
        )

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Notification.objects.all().delete()

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user1)

    def test_get_update_list(self):
        """
        Compares the test data to what is actually returned from GET
        """
        response = self.client.get('/updates/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 3)

        expected_reponse_json = \
            [self.data_to_list_represent(self.test_data["updates"][0]),
             self.data_to_list_represent(self.test_data["updates"][1]),
             self.data_to_list_represent(self.test_data["updates"][3])]
        self.assertEqual(expected_reponse_json, response.json())

    def test_get_update_list_query_args(self):
        """
        Compares the test data to what is actually returned from GET with
        query params
        """
        response = self.client.get("/updates/?parent_notification={0}".format(
            self.test_data["notifications"][0]["id"]
        ))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.json()), 2)

        expected_reponse_json = \
            [self.data_to_list_represent(self.test_data["updates"][0]),
             self.data_to_list_represent(self.test_data["updates"][1])]
        self.assertEqual(expected_reponse_json, response.json())

    def test_get_update_detail_by_id(self):
        """
        Compares the test data to what is actually returned from GET
        at an id endpoint
        """
        response = self.client.get("/updates/{0}/".format(
            self.test_data["updates"][0]["id"]
        ))

        self.assertEqual(response.status_code, 200)

        expected_reponse_json = self.data_to_detail_represent(
            self.test_data["updates"][0],
            response.json()["created_time"]
        )
        self.assertEqual(expected_reponse_json, response.json())

    def test_get_update_detail_by_bad_id(self):
        """
        Compares the test data to what is actually returned from GET
        at an id endpoint
        """
        response = self.client.get("/updates/100/")

        self.assertEqual(response.status_code, 404)

    def test_post_valid_update(self):
        """
        Attempts to post a valid notification payload and tests that the
        request is successful and the response json is matches the request
        data
        """
        payload = self.data_to_payload_represent(self.test_data["updates"][4])

        with generate_twilio_mock() as mock:
            response = self.client.post("/updates/", payload)
            self.assertEqual(response.status_code, 201)

            self.test_data["updates"][4]["id"] = response.json()["id"]
            expected_reponse_json = self.data_to_detail_represent(
                self.test_data["updates"][4],
                response.json()["created_time"]
            )

            self.assertEqual(expected_reponse_json, response.json())

            response2 = self.client.get("/updates/{0}/".format(
                self.test_data["updates"][4]["id"]
            ))

            self.assertEqual(response2.status_code, 200)
            self.assertEqual(response.json(), response2.json())

    """
    def test_create_update(self):
        valid_payload = {
            "text": "test update",
            "parent_notification": self.notification.id
        }
        original_len = len(Update.objects.all())

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

            response = self.client.post('/updates/',
                                        data=json.dumps(valid_payload),
                                        content_type='application/json')
            self.assertEqual(201, response.status_code)
            application/json
            updated_len = len(Update.objects.all())
            self.assertEqual(updated_len - original_len, 1)
            model = Update.objects.get(parent_notification=self.notification)
            self.assertEqual(model.text, valid_payload["text"])

    def test_read_update(self):
        update = Update.objects.create(
            text="test update",
            parent_notification=self.notification
        )
        response = self.client.get('/updates/')
        self.assertEqual(200, response.status_code)
        data = response.data[0]
        self.assertEqual(data["text"], "test update")
        self.assertEqual(data["parent_notification"], self.notification.id)"""

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

    def data_to_payload_represent(self, data, ended=None):
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
        if ended is not None:
            payload["ended"] = ended

        return payload
