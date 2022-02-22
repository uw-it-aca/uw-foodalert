# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.test import TestCase, Client
from parameterized import parameterized, param
from unittest.mock import patch

from foodalert.sender import Sender


class SendMailTest(TestCase):

    @patch('dbmail.send_db_mail')
    def test_send():
        Sender.send_email("test", ["javerage@uw.edu"], '123456789')
        assert dbmail.send_db_mail.called
