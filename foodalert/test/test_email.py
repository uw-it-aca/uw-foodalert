# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
from django.test import TestCase, Client
from django.test.utils import override_settings
from django.db import connection
from django.conf import settings
from unittest.mock import patch, Mock
from dbmail import send_db_mail
from dbmail.models import MailTemplate, MailLog, MailLogEmail
from django.core.exceptions import ValidationError
from django.core.mail import send_mail


class EmailTest(TestCase):
    @classmethod
    def setUpClass(cls):
        MailTemplate.objects.create(
            name="Test template",
            subject="New UW Food Alert Event: Test Event is Open",
            message="Just a quick test",
            slug="test",
        )
        MailTemplate.objects.create(
            name="Test template2",
            subject="New UW Food Alert Event: {{event}} is Open",
            message="Serving: {{food}}, at {{location}}",
            slug="temp",
        )

    @classmethod
    def tearDownClass(cls):
        MailTemplate.objects.all().delete()
        MailLog.objects.all().delete()

    def test_send_email_basic(self):
        """
        Basic test of sending an email using
        django-db-mailer
        """
        mail = send_db_mail(
            slug="test",
            recipient='javerage@uw.edu',
        )
        self.assertEquals(mail, 'OK')

    def test_send_templated_email(self):
        """
        Tests that emails sent with additional arguments
        template the given arguments into the email
        correctly
        """
        mail = send_db_mail(
            "temp",
            "javerage@uw.edu",
            {
                'event': 'Test Event',
                'food': 'Hawaiian pizza',
                'location': 'HUB 120'
            },
        )
        self.assertEquals(mail, 'OK')

    def test_send_with_bcc(self):
        """
        Tests that emails sent with a bcc list
        are sent correctly when provided a list of
        recipients
        """
        mail = send_db_mail(
            slug="test",
            recipient="javerage@uw.edu",
            bcc=['keithrob@uw.edu', 'test@uw.edu']
        )

        self.assertEquals(mail, 'OK')
