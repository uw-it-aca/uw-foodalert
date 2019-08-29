import json
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from django.db import connection, transaction
from django.conf import settings

import foodalert
from foodalert.models import Allergen
from foodalert.serializers import AllergenSerializer
from foodalert.views import AllergensList
from foodalert.test.test_utils import create_user_and_client_from_data

create_group = settings.FOODALERT_AUTHZ_GROUPS['create']
audit_group = settings.FOODALERT_AUTHZ_GROUPS['audit']


class AllergenTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(
            username="testuser1",
            email="testuser1@test.com",
            password="test",
            is_active=1
        )
        cls.realAllergen = Allergen.objects.create(
            name="test allergen"
        )

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Allergen.objects.all().delete()

    def test_get_allergen_list(self):
        """
        This tests that you can read all allergens
        in the db from a get request. Should return a
        200 response upon success
        """
        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [create_group, audit_group]}
        session.save()

        response = client.get('/allergen/')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(data[0]["name"], self.realAllergen.name)

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [audit_group]}
        session.save()

        response = client.get('/allergen/')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(data[0]["name"], self.realAllergen.name)

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [create_group]}
        session.save()

        response = client.get('/allergen/')
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(data[0]["name"], self.realAllergen.name)

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": []}
        session.save()

        response = client.get('/allergen/')
        self.assertEqual(403, response.status_code)

    def test_post_allergen(self):
        """
        This tests that an allergen should be created
        correctly from post request. Should return a 201
        response upon success
        """
        valid_payload = {
            "name": "wheat"
        }

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": []}
        session.save()

        original_len = len(Allergen.objects.all())
        response = client.post('/allergen/', valid_payload)
        self.assertEqual(403, response.status_code)
        new_len = len(Allergen.objects.all())
        self.assertEqual(new_len, original_len)

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [create_group]}
        session.save()

        original_len = len(Allergen.objects.all())
        response = client.post('/allergen/', valid_payload)
        self.assertEqual(403, response.status_code)
        new_len = len(Allergen.objects.all())
        self.assertEqual(new_len, original_len)

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [audit_group]}
        session.save()

        original_len = len(Allergen.objects.all())
        response = client.post('/allergen/', valid_payload)
        self.assertEqual(403, response.status_code)
        new_len = len(Allergen.objects.all())
        self.assertEqual(new_len, original_len)

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [create_group, audit_group]}
        session.save()

        original_len = len(Allergen.objects.all())
        response = client.post('/allergen/', valid_payload)
        self.assertEqual(403, response.status_code)
        new_len = len(Allergen.objects.all())
        self.assertEqual(new_len, original_len)

        self.user.is_staff = True
        self.user.save()

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": []}
        session.save()

        original_len = len(Allergen.objects.all())
        response = client.post('/allergen/', valid_payload)
        self.assertEqual(201, response.status_code)
        new_len = len(Allergen.objects.all())
        self.assertEqual(1, new_len - original_len)
        posted_allergen = response.json()
        self.assertEqual(posted_allergen["name"], valid_payload["name"])

        self.user.is_staff = False
        self.user.save()

    def test_post_existing_allergen(self):
        """
        Test should return a 400 bad request error if post request contains
        anallergen name that already exists in the database. New object
        should not be made
        """
        self.user.is_staff = True
        self.user.save()

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [create_group, audit_group]}
        session.save()

        original_len = len(Allergen.objects.all())
        data_before = client.get("/allergen/")
        payload = {
            "name": self.realAllergen.name
        }
        response = client.post('/allergen/', payload)
        self.assertEqual(400, response.status_code)
        after_len = len(Allergen.objects.all())
        self.assertEqual(original_len, after_len)
        data_after = client.get('/allergen/')
        self.assertEqual(data_before.json(), data_after.json())

        self.user.is_staff = False
        self.user.save()

    def test_invalid_put_allergen(self):
        """
        This tests that allergens should not be alterable after
        they are entered into the db. Put requests to /allergen/
        endpoint should return a 403 resposnse
        """
        self.user.is_staff = True
        self.user.save()

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [create_group, audit_group]}
        session.save()

        invalidRequest = {
            "name": "put update"
        }
        response = client.put('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)

        self.user.is_staff = False
        self.user.save()

    def test_invalid_patch_allergen(self):
        """
        This tests that you allergens should not be
        alterable after they are entered into the db.
        Patch requests should return a 403 resposnse
        """
        self.user.is_staff = True
        self.user.save()

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [create_group, audit_group]}
        session.save()

        invalidRequest = {
            "name": "patch update"
        }
        response = client.patch('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)

        self.user.is_staff = False
        self.user.save()

    def test_invalid_delete_allergen(self):
        """
        This tests that you can delete a single
        allergen from the db. Should return a 403 response
        """
        self.user.is_staff = True
        self.user.save()

        client = Client()
        client.force_login(self.user)
        session = client.session
        session['samlUserdata'] = {"isMemberOf": [create_group, audit_group]}
        session.save()

        original_len = len(Allergen.objects.all())
        invalidRequest = {
            "name": "delete update"
        }
        after_len = len(Allergen.objects.all())
        response = client.delete('/allergen/', invalidRequest)
        self.assertEqual(405, response.status_code)
        self.assertEqual(original_len, after_len)

        self.user.is_staff = False
        self.user.save()
