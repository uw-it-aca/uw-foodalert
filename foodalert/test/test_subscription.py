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
        """Tests that subscription model can be created successfully"""
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
        """Subscription model cannot be created with invalid parameters"""
        with self.assertRaises(IntegrityError):
            sub = Subscription.objects.create(
                user=self.user,
                email=email,
                sms_number=sms
            )

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_post_subscription(self, email=None, sms=None):
        """
        Tests that subscription object is correctly created in db by
        sending a post request to the '/subscription/' endpoint. Post
        request should return 201 status code
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
    def test_invalid_post_subscription(self, email='', sms=''):
        """
        Post request should not be made to '/subsription/{id}/' endpoint.
        Request should return a 405 error
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )
        invalid_payload = {
            "email": "invalidemailpost@test.com",
            "sms": "+14083429456",
        }
        original_len = len(Subscription.objects.all())
        original_data = self.client.get('/subscription/{}/'.format(sub.id))
        original_data = original_data.json()
        response = self.client.post('/subscription/{}/'.format(sub.id),
                                    data=json.dumps(invalid_payload),
                                    content_type='application/json')
        self.assertEqual(405, response.status_code)
        after_len = len(Subscription.objects.all())
        self.assertEqual(original_len, after_len)
        after_data = self.client.get('/subscription/{}/'.format(sub.id))
        after_data = after_data.json()
        self.assertEqual(original_data, after_data)

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
        """
        A patch request to update either sms or email is valid. The fields in
        the payload should be the only fields that are updated
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )
        patch_id = sub.id

        email_before = sub.email
        payload = {
            "sms_number": "+14084388625"
        }
        original_len = len(Subscription.objects.all())
        response = self.client.patch('/subscription/{}/'.format(patch_id),
                                     data=json.dumps(payload),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        after_len = len(Subscription.objects.all())
        self.assertEqual(original_len, after_len)
        data = response.json()
        self.assertEqual(payload['sms_number'], data['sms_number'])
        self.assertEqual(email_before, data['email'])

        get_res = self.client.get('/subscription/{}/'.format(patch_id))
        updated_data = get_res.json()
        self.assertEqual(updated_data['sms_number'], payload['sms_number'])

        payload2 = {
            "email": "practice@mail.com"
        }
        sms_before = updated_data['sms_number']
        original_len = len(Subscription.objects.all())
        response = self.client.patch('/subscription/{}/'.format(patch_id),
                                     data=json.dumps(payload2),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        after_len = len(Subscription.objects.all())
        self.assertEqual(original_len, after_len)
        data = response.json()
        self.assertEqual(payload2['email'], data['email'])
        self.assertEqual(sms_before, data['sms_number'])

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_verified_patch_subscription(self, email='', sms=''):
        """
        If user has a verified email or number, they should be able to
        change the value of 'notif_on' with a patch request.
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms,
            email_verified=True,
        )
        notif_state = sub.notif_on
        valid_payload = {
            'notif_on': not notif_state
        }
        response = self.client.patch('/subscription/{}/'.format(sub.id),
                                     data=json.dumps(valid_payload),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(valid_payload['notif_on'], data['notif_on'])

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_unverified_patch_subscription(self, email='', sms=''):
        """
        If user does not have a verified email or number, they should not
        be able to change the value of 'notif_on' with a patch request.
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms,
        )
        notif_state = sub.notif_on
        valid_payload = {
            'notif_on': not notif_state
        }
        response = self.client.patch('/subscription/{}/'.format(sub.id),
                                     data=json.dumps(valid_payload),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(notif_state, data['notif_on'])

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_invalid_patch_subscription(self, email='', sms=''):
        """
        Tests that email_verified and number_verified value cannot be changed
        from patch request. Ensures that it is a read_only_field
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
        invalid_payload = {
            'email_verified': not email_verif_state,
            'number_verified': not sms_verif_state
        }

        response = self.client.patch('/subscription/{}/'.format(patch_id),
                                     data=json.dumps(invalid_payload),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(email_verif_state, data['email_verified'])
        self.assertEqual(sms_verif_state, data['number_verified'])

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_put_subscription(self, email=None, sms=None):
        """
        Tests that you can make updates to subscription by making
        put request to '/subscription/{id}/' endpoint
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms
        )
        original_len = len(Subscription.objects.all())
        payload = {
            'email': 'putEmail@mail.com',
            'sms_number': '+13438765646'
        }
        response = self.client.put('/subscription/{}/'.format(sub.id),
                                   data=payload,
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(payload['email'], data['email'])
        self.assertEqual(payload['sms_number'], data['sms_number'])
        after_len = len(Subscription.objects.all())
        self.assertEqual(original_len, after_len)

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_unsubscribe(self, email=None, sms=None):
        """
        Patch request successfully empties both sms and email fields
        """
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
        response = self.client.patch('/subscription/{}/'.format(sub.id),
                                     data=json.dumps(update),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        new_len = len(Subscription.objects.all())
        self.assertEqual(original_len, new_len)

        sub = Subscription.objects.get(pk=sub.id)

        self.assertEqual(update['email'], sub.email)
        self.assertEqual(update['sms_number'], sub.sms_number)

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_verified_unsubscribe(self, email=None, sms=None):
        """
        Patch request successfully empties both sms and email fields.
        When input is emptied, its verified state should be false.
        If both fields are empty, both verified states should be false
        rendering notif_on to be false too
        """
        sub = Subscription.objects.create(
            user=self.user,
            email=email,
            sms_number=sms,
            email_verified=True,
            number_verified=True,
            notif_on=True
        )

        update = {
            'email': '',
            'sms_number': '',
        }

        original_len = len(Subscription.objects.all())
        response = self.client.patch('/subscription/{}/'.format(sub.id),
                                     data=json.dumps(update),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        new_len = len(Subscription.objects.all())
        self.assertEqual(original_len, new_len)

        sub = Subscription.objects.get(pk=sub.id)

        self.assertEqual(update['email'], sub.email)
        self.assertEqual(update['sms_number'], sub.sms_number)
        self.assertFalse(sub.email_verified)
        self.assertFalse(sub.number_verified)
        self.assertFalse(sub.notif_on)

    @parameterized.expand(VALID_TEST_CASES)
    @transaction.atomic
    def test_delete_subscription(self, email=None, sms=None):
        """
        Tests that you can successfully delete a subscription
        from the db. Delete request to '/subscription/{id}/'
        endpoint should return a 204 status code
        """
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
