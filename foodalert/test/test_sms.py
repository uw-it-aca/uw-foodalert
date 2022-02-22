# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0
import os
import json
from datetime import datetime
from django.test import TestCase
from foodalert.sender import Sender


class SMSTest(TestCase):
    def test_format_message(self):
        """
        Tests the format message function used to format
        a notification instance into a readable text
        """
        data = {
            'location': 'UW Campus',
            'event': 'UW Event',
            'time': {
                'end': datetime.strptime('2019-12-13T20:23:06.200-+0000',
                                         "%Y-%m-%dT%H:%M:%S.%f-%z"),
            },
            'food': {
                'served': 'Sandwitches',
                'allergens': ['wheat', 'fish', 'peanuts']
            },
            'bring_container': True,
        }

        expected = ("Food available: UW Event\n"
                    "Sandwitches\n\n"
                    "End time: 12:23 PM\n"
                    "Location: UW Campus\n"
                    "May contain: wheat, fish, peanuts\n\n"
                    "You must bring a container.\n\n"
                    "Thanks,\n"
                    "UW Food Alert")

        message = Sender.format_message(data)
        self.assertEquals(message, expected)
