from django.test import TestCase, Client
from parameterized import parameterized, param
from unittest.mock import patch

from foodalert.sender import Sender


class SendMailTest(TestCase):

    @patch('dbmail.send_db_mail')
    def test_send():
        Sender.send_email("test", ["javerage@uw.edu"])
        assert dbmail.send_db_mail.called
