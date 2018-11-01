import os
import json
from django.test import TestCase, Client
from parameterized import parameterized
from django.db import connection
from django.contrib.auth.models import User

import foodalert
from foodalert.models import *
from foodalert.serializers import *

RESOURCE_DIR = os.path.join(os.path.dirname(foodalert.__file__),
                            'test',
                            'resources')


class SubscriptionTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up a single mock user that can be used for all tests on
        notification tests
        """
        cls.user = User.objects.create_user(username='testuser',
                                            email="testuser@test.com",
                                            password="test")

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    @parameterized.expand([
        ("testuser@test.com", "+41524204242"),
        ("testuser@test.com", ""),
        ("", "+41524204242"),
        ("", ""),
    ])
    def test_subscription_model(self, email, sms):
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )
        self.assertEqual(sub.email, email)
        self.assertEqual(sub.sms_number, sms)

    def test_create_subscription(self):
        pass

    def test_read_subscription(self):
        pass

    def test_update_subscription(self):
        pass

    def test_delete_subscription(self):
        pass
