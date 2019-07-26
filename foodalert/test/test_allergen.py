from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
#from parameterized import parameterized, param
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

    def setUp(self):
        self.client.force_login(self.user)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

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

    def test_get_allergen_list(self):
        """
        This tests that you can read all allergens
        in the db from a get request. Should return a 
        200 response upon success
        """
        newAllergen = Allergen.objects.create(
                name= "test allergen"
                )
        response = self.client.get('/allergen/')
        self.assertEqual(200, response.status_code)
        data = response.data[0]
        self.assertEqual(data["name"], "test allergen")

    def test_invalid_put_allergen(self):
        """
        This tests that you allergens should not be 
        alterable after they are entered into the db.
        Put requests should return a 405 resposnse
        """
        invalidRequest = {
            "name": "update"
        }
        response = self.client.put('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)

    def test_invalid_patch_allergen(self):
        """
        This tests that you allergens should not be 
        alterable after they are entered into the db.
        Patch requests should return a 405 resposnse
        """
        invalidRequest = {
            "name": "update"
        }
        response = self.client.patch('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)

    def test_invalid_delete_allergen(self):
        """
        This tests that you can delete a single
        allergen from the db. Should return a 200 response
        after successfully deleting
        """
        newAllergen = Allergen.objects.create(name = "test allergen")
        original_len = len(Allergen.objects.all())
        invalidRequest = {
            "name": "test allergen"
        }
        after_len = len(Allergen.objects.all())
        response = self.client.delete('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)
        self.assertEqual(original_len, after_len)