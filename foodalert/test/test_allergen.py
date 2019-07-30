import json
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from django.db import connection, transaction

import foodalert
from foodalert.models import Allergen
from foodalert.serializers import AllergenSerializer
from foodalert.views import AllergensList


class AllergenTest(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Sets up a single mock user that can be used for all tests on
        notification tests
        """
        user = "testuser1"
        passw = "test"
        cls.user = User.objects.create_user(username=user,
                                            email="testuser1@test.com",
                                            password=passw,
                                            is_active=1)
        cls.realAllergen = Allergen.objects.create(
                name="test allergen"
                )

    def setUp(self):
        self.client = Client()
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        cls.realAllergen.delete()

    def tearDown(self):
        pass

    def test_get_allergen_list(self):
        """
        This tests that you can read all allergens
        in the db from a get request. Should return a
        200 response upon success
        """
        response = self.client.get('/allergen/')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(data[0]["name"], self.realAllergen.name)

    def test_get_allergen_detail(self):
        """
        This tests that you can read allergen detail
        corresponding to the id
        """
        get_id = self.realAllergen.id
        response = self.client.get('/allergen/{}/'.format(get_id))
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(self.realAllergen.name, data["name"])

    def test_post_allergen(self):
        """
        This tests that an allergen should be created
        correctly from post request. Should return a 201
        response upon success
        """
        valid_payload = {
            "name": "wheat"
        }
        original_len = len(Allergen.objects.all())
        response = self.client.post('/allergen/', valid_payload)
        self.assertEqual(201, response.status_code)
        new_len = len(Allergen.objects.all())
        self.assertEqual(1, new_len - original_len)
        posted_allergen = response.json()
        self.assertEqual(posted_allergen["name"], valid_payload["name"])
        post_id = response.json()["id"]
        get_res = self.client.get('/allergen/{}/'.format(post_id))
        res = get_res.json()
        self.assertEqual(res["name"], valid_payload["name"])

    def test_post_existing_allergen(self):
        """
        Test should return a 400 bad request error if post request contains
        anallergen name that already exists in the database. New object
        should not be made
        """
        original_len = len(Allergen.objects.all())
        data_before = self.client.get("/allergen/")
        payload = {
            "name": self.realAllergen.name
        }
        response = self.client.post('/allergen/', payload)
        self.assertEqual(400, response.status_code)
        after_len = len(Allergen.objects.all())
        self.assertEqual(original_len, after_len)
        data_after = self.client.get('/allergen/')
        self.assertEqual(data_before.json(), data_after.json())

    def test_invalid_put_allergen(self):
        """
        This tests that allergens should not be alterable after
        they are entered into the db. Put requests to /allergen/
        endpoint should return a 405 resposnse
        """
        invalidRequest = {
            "name": "put update"
        }
        response = self.client.put('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)

    def test_put_allergen_with_id(self):
        """
        This tests that you are able to make changes to an
        allergen with a put request to the endpoint '/allergen/{id}/'
        Request should return a 200 success status code
        """
        payload = {
            "name": "put update"
        }
        before_len = len(Allergen.objects.all())
        put_id = self.realAllergen.id
        response = self.client.put('/allergen/{}/'.format(put_id),
                                   json.dumps(payload),
                                   content_type='application/json')
        self.assertEqual(200, response.status_code)
        after_len = len(Allergen.objects.all())
        self.assertEqual(before_len, after_len)
        put_result = self.client.get('/allergen/{}/'.format(put_id))
        put_result = put_result.json()
        self.assertEqual(put_result['name'], payload['name'])
        self.assertEqual(put_result['id'], put_id)

    def test_invalid_patch_allergen(self):
        """
        This tests that you allergens should not be
        alterable after they are entered into the db.
        Patch requests should return a 405 resposnse
        """
        invalidRequest = {
            "name": "patch update"
        }
        response = self.client.patch('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)

    def test_patch_allergen_with_id(self):
        """
        This tests that you should be able to alter an allergen
        with a patch request to '/allergen/{id}/' endpoint.
        Should return a 200 success status code
        """
        payload = {
            "name": "patch update"
        }
        before_len = len(Allergen.objects.all())
        patch_id = self.realAllergen.id
        response = self.client.patch('/allergen/{}/'.format(patch_id),
                                     json.dumps(payload),
                                     content_type='application/json')
        self.assertEqual(200, response.status_code)
        after_len = len(Allergen.objects.all())
        self.assertEqual(before_len, after_len)
        patch_result = self.client.get('/allergen/{}/'.format(patch_id))
        patch_result = patch_result.json()
        self.assertEqual(patch_result['name'], payload['name'])
        self.assertEqual(patch_result['id'], patch_id)

    def test_invalid_delete_allergen(self):
        """
        This tests that you can delete a single
        allergen from the db. Should return a 200 response
        after successfully deleting
        """
        original_len = len(Allergen.objects.all())
        invalidRequest = {
            "name": "delete update"
        }
        after_len = len(Allergen.objects.all())
        response = self.client.delete('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)
        self.assertEqual(original_len, after_len)

    def test_delete_allergen_with_id(self):
        """
        This tests that you should be able to delete an allergen
        with a delete request to the '/allergen/{id}/' endpoint
        """
        original_len = len(Allergen.objects.all())
        delete_id = self.realAllergen.id
        response = self.client.delete('/allergen/{}/'.format(delete_id))
        after_len = len(Allergen.objects.all())
        self.assertEqual(204, response.status_code)
        self.assertEqual(1, original_len - after_len)
