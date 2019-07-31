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
        data = response.json()
        self.assertEqual("testuser@test.com", data[0]['netid'])
        self.assertEqual(sub.id, data[0]["id"])
        # get response should just return id and netid
        data_len = len(data[0])
        self.assertEqual(data_len, 2)

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_get_subscription_detail(self, email='', sms=''):
        """
        Calling get request to '/subscription/{id}/' endpoint should return
        a 200 status code. Returns json containing id, netid, email/sms,
        email/sms verified state, and notif on state
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )

        sub_id = sub.id
        response = self.client.get('/subscription/{}/'.format(sub_id))
        self.assertEqual(200, response.status_code)
        data = response.json()
        # email and sms should be updated with correct values
        self.assertEqual(sub.email, data["email"])
        self.assertEqual(sub.sms_number, data["sms_number"])
        # all boolean fields should be false at this point
        self.assertFalse(data["email_verified"])
        self.assertFalse(data["number_verified"])
        self.assertFalse(data["notif_on"])

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_patch_subscription(self, email=None, sms=None):
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )

        payload = {
            "sms_number": "+14084388625"
        }
        patch_id = sub.id

        original_len = len(Subscription.objects.all())
        response = self.client.patch('/subscription/{}/'.format(patch_id),
                                     data=json.dumps(payload),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        after_len = len(Subscription.objects.all())
        self.assertEqual(original_len, after_len)
        data = response.json()
        self.assertEqual(payload['sms_number'], data['sms_number'])

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_invalid_patch_subscription(self, email='', sms=''):
        """
        Tests that email_verified value cannot be changed from patch
        request. Ensures that it is a read_only_field
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )
        patch_id = sub.id
        # current value of read only fields
        get_res = self.client.get('/subscription/{}/'.format(patch_id))
        email_verif_state = get_res.json()['email_verified']
        sms_verif_state = get_res.json()['number_verified']
        notif_state = get_res.json()['notif_on']
        invalid_payload = {
            'email_verified': not email_verif_state,
            'number_verified': not sms_verif_state,
            'notif_state': not notif_state
        }

        response = self.client.patch('/subscription/{}/'.format(patch_id),
                                     data=json.dumps(invalid_payload),
                                     content_type='application/json')
        data = response.json()
        self.assertEqual(email_verif_state, data['email_verified'])
        self.assertEqual(sms_verif_state, data['number_verified'])
        self.assertEqual(notif_state, data['notif_on'])

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
