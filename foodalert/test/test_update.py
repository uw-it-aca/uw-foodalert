import os
import json
from django.test import TestCase, Client
from parameterized import parameterized, param
from django.db import connection, transaction
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

import foodalert
from foodalert.models import Update, Notification
from foodalert.serializers import UpdateSerializer
from foodalert.views import UpdateDetail, UpdateList
from foodalert.sender import TwilioSender
from unittest.mock import patch, Mock, PropertyMock

"""
Stuff to test:
Real points

GET /update/
    - Test the format is right when multiple updates are listed.
GET /update/?parent_notification_id=<integer>
    - Test the format is right when multiple updates are listed.
    - Test that only the relevent updates are listed
    - Test that only children of notificatons created by the user are accessible
GET /update/<id>/
    - Test that the right json is returned
    - Test the case when the element with that id does not exist
POST /update/
    - Test if this action creates an update.
    - Test if multiple updates are created porperly
    - Test an update request with fields missing.
    - Test that a update with ended: true ends and notification
    - Test that an update with ended: false dosen't affect the notification
    - Test that no more updates can be created under an ended notificaitons
    - Test that ended: true always creates the same message.

405 points

POST /update/<id>
PUT /update/
PUT /update/<id>
PATCH /update/
PATCH /update/<id>
DELETE /update/
DELETE /update/<id>
"""

VALID_TEST_CASES = [
    param(text="test update"),
]

INVALID_TEST_CASES = [
    param(parent_notification=""),
    param(),
]


class UpdateTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up a mock user for testing API calls
        to the update endpoint
        """
        cls.user = User.objects.create_user(username="testuser",
                                            email="testuser@test.com",
                                            password="test")

        cls.notification = Notification.objects.create(
            location="UW Campus",
            event="UW Event",
            food_served="Food",
            amount_of_food_left="No Food",
            host=cls.user,
            host_user_agent="browser")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.notification.delete()

    @transaction.atomic
    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    @transaction.atomic
    def tearDown(self):
        Update.objects.all().delete()

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_valid_update_models(self, text=None):
        update = Update.objects.create(
            text=text,
            parent_notification=self.notification
        )
        self.assertEqual(update.text, text)
        self.assertEqual(update.parent_notification, self.notification)

    @parameterized.expand(INVALID_TEST_CASES)
    @transaction.atomic
    def test_invalid_update_models(self, text=None, parent_notification=None):
        with self.assertRaises((IntegrityError, ValueError)):
            update = Update.objects.create(
                text=text,
                parent_notification=parent_notification
            )

    @transaction.atomic
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

            updated_len = len(Update.objects.all())
            self.assertEqual(updated_len - original_len, 1)
            model = Update.objects.get(parent_notification=self.notification)
            self.assertEqual(model.text, valid_payload["text"])

    @transaction.atomic
    def test_read_update(self):
        update = Update.objects.create(
            text="test update",
            parent_notification=self.notification
        )
        response = self.client.get('/updates/')
        self.assertEqual(200, response.status_code)
        data = response.data[0]
        self.assertEqual(data["text"], "test update")
        self.assertEqual(data["parent_notification"], self.notification.id)
