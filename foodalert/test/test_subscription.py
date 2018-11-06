import os
import json
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from parameterized import parameterized, param
from django.db import connection
from django.db.utils import IntegrityError
from django.contrib.auth.models import User

import foodalert
from foodalert.models import Subscription
from foodalert.serializers import SubscriptionSerializer
from foodalert.views import SubscriptionDetail, SubscriptionList

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

    @parameterized.expand(VALID_TEST_CASES)
    def test_create_subscription(self, email=None, sms=None):
        factory = APIRequestFactory()
        valid_payload = {
            "netId": "testuser@test.com",
            "email": email,
            "sms": sms,
        }
        request = factory.post('/subscription/', valid_payload, format='json')
        request.user = self.user
        original_len = len(Subscription.objects.all())
        response = SubscriptionList.as_view()(request)
        self.assertEqual(201, response.status_code)
        new_len = len(Subscription.objects.all())
        self.assertEqual(1, new_len - original_len)
        model = Subscription.objects.get(user=self.user)
        self.assertEqual("testuser@test.com", model.netid)
        self.assertEqual(email, model.email)
        self.assertEqual(sms, model.sms_number)

    def test_read_subscription(self):
        pass

    def test_update_subscription(self):
        pass

    def test_delete_subscription(self):
        pass
