import os
import json
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
from parameterized import parameterized, param
from django.db import connection, transaction
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
        user = "testuser"
        passw = "test"
        cls.user = User.objects.create_user(username=user,
                                            email="testuser@test.com",
                                            password=passw)

        cls.client = Client()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    @transaction.atomic
    def setUp(self):
        self.client.force_login(self.user)

    @transaction.atomic
    def tearDown(self):
        Subscription.objects.all().delete()

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_valid_subscription_models(self, email=None, sms=None):
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )
        self.assertEqual(sub.email, email)
        self.assertEqual(sub.sms_number, sms)

    @parameterized.expand(INVALID_TEST_CASES)
    @transaction.atomic
    def test_invalid_subscription_models(self, email=None, sms=None):
        with self.assertRaises(IntegrityError):
            sub = Subscription.objects.create(
                user=self.user,
                email=email,
                sms_number=sms
            )

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_create_subscription(self, email=None, sms=None):
        valid_payload = {
            "netId": "testuser@test.com",
            "email": email,
            "sms": sms,
        }
        original_len = len(Subscription.objects.all())
        response = self.client.post('/subscription/', valid_payload)
        self.assertEqual(201, response.status_code)
        new_len = len(Subscription.objects.all())
        self.assertEqual(1, new_len - original_len)
        model = Subscription.objects.get(user=self.user)
        self.assertEqual("testuser@test.com", model.netid)
        self.assertEqual(email, model.email)
        self.assertEqual(sms, model.sms_number)

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_read_subscription(self, email='', sms=''):
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )

        response = self.client.get('/subscription/')
        self.assertEqual(200, response.status_code)
        data = response.data[0]
        self.assertEqual(email, data['email'])
        self.assertEqual(sms, data['sms_number'])
        self.assertEqual("testuser@test.com", data['netid'])

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_update_subscription(self, email=None, sms=None):
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )

        update = {
            'id': sub.id,
            'email': 'prefix-' + sub.email,
            'sms': '+12345678901',
        }

        original_len = len(Subscription.objects.all())
        response = self.client.put('/subscription/{0}/'.format(sub.id),
                                   data=json.dumps(update),
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)
        new_len = len(Subscription.objects.all())
        self.assertEqual(original_len, new_len)

        sub = Subscription.objects.get(pk=sub.id)

        self.assertEqual(update['email'], sub.email)
        self.assertEqual(update['sms'], sub.sms_number)

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_delete_subscription(self, email=None, sms=None):
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )

        original_len = len(Subscription.objects.all())
        response = self.client.delete('/subscription/{0}/'.format(sub.id))
        self.assertEqual(204, response.status_code)
        new_len = len(Subscription.objects.all())
        self.assertEqual(original_len - 1, new_len)
        model_list = Subscription.objects.all().filter(pk=sub.id)
        self.assertEqual(0, len(model_list))
