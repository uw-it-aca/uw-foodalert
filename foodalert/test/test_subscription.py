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
        """
        Tests that subscription object is correctly created in db by
        sending a post request to the '/subscription/' endpoint. Post
        request should return a 200 status code
        """
        valid_payload = {
            "email": email,
            "sms_number": sms,
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
    def test_get_subscriptionlist(self, email='', sms=''):
        """
        Tests that subscription list is returned from a get
        request to '/subscription/' endpoint. Request should return
        a 200 status code and the id and netid of each subscription.
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )

        response = self.client.get('/subscription/')
        self.assertEqual(200, response.status_code)
        data = response.data[0]
        self.assertEqual("testuser@test.com", data['netid'])
        self.assertEqual(sub.id, data["id"])

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_update_subscription(self, email=None, sms=None):
        """
        Tests that subscription is correctly updated. Only sms or
        email should be altered by the user

        -->NOTE: RIGHT NOW POST IS DOING WHAT PATCH/PUT IS DOING....
        WRITE TESTS FOR SPECIFICALLY PATCH/PUT

        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )

        update = {
            'email': 'prefix-' + sub.email,
            'sms_number': ' +12024561414',
        }

        original_len = len(Subscription.objects.all())
        response = self.client.post('/subscription/',
                                    data=json.dumps(update),
                                    content_type='application/json')
        self.assertEqual(201, response.status_code)
        new_len = len(Subscription.objects.all())
        self.assertEqual(original_len, new_len)

        sub = Subscription.objects.get(pk=sub.id)

        self.assertEqual(update['email'], sub.email)
        self.assertEqual(update['sms_number'], sub.sms_number)

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_unsubscribe(self, email=None, sms=None):
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )

        update = {
            'email': '',
            'sms_number': '',
        }

        original_len = len(Subscription.objects.all())
        response = self.client.post('/subscription/',
                                    data=json.dumps(update),
                                    content_type='application/json')
        self.assertEqual(201, response.status_code)
        new_len = len(Subscription.objects.all())
        self.assertEqual(original_len, new_len)

        sub = Subscription.objects.get(pk=sub.id)

        self.assertEqual(update['email'], sub.email)
        self.assertEqual(update['sms_number'], sub.sms_number)

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
