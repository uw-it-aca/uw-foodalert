import os
import json
from django.test import TestCase, Client
from parameterized import parameterized, param
from django.db import connection
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

import foodalert
from foodalert.models import *
from foodalert.serializers import *

VALID_TEST_CASES = [
    param(email="testuser@test.com", sms="+41524204242"),
    param(sms="+41524204242", email=""),
    param(email="testuser@test.com", sms=""),
]

INVALID_TEST_CASES = [
    param(sms="+41524204242"),
    param(email="testuser@test.com"),
    param(),
]

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
        Subscription.objects.all().delete()

    @parameterized.expand(VALID_TEST_CASES)
    def test_valid_subscription_models(self, email=None, sms=None):
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )
        self.assertEqual(sub.email, email)
        self.assertEqual(sub.sms_number, sms)

    @parameterized.expand(INVALID_TEST_CASES)
    def test_invalid_subscription_models(self, email=None, sms=None):
        with self.assertRaises(IntegrityError):
            sub = Subscription.objects.create(
                user=self.user,
                email=email,
                sms_number=sms
            )

    def test_create_subscription(self):
        pass

    def test_read_subscription(self):
        pass

    def test_update_subscription(self):
        pass

    def test_delete_subscription(self):
        pass
