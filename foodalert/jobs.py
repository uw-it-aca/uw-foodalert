# Copyright 2022 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import time
import logging
from dateutil import parser
from django.conf import settings
from django_dbq.models import Job
from foodalert.models import Subscription
from foodalert.sender import Sender

debug_mode = getattr(settings, 'DEBUG')

logger = logging.getLogger(__name__)


def queue_messages(job):

    # Retreive users email/sms Subscription status
    email_recipients = []
    sms_recipients = []
    for sub in Subscription.objects.all():
        if sub.send_email:
            email_recipients.append(sub.email)
        if sub.send_sms:
            sms_recipients.append(str(sub.sms_number))

    # Handle the formatting of messages based on
    # if the message is for a Notifcation or Update
    data = job.workspace['data']
    email = {}
    sms = ''
    slug = ''

    if job.workspace['update']:
        # Update

        # Email formatting
        email['name'] = "Food Alert Update"
        subj = "[UW Food Alert] Update: {}, {}"
        email['subject'] = subj.format(job.workspace['event'],
                                       job.workspace['location'])
        email['body'] = ('Update: ' + data['text'] + '\n\n'
                         'Thanks,\n'
                         'UW Food Alert')

        # SMS formatting
        sms = job.workspace['event'] + ' Update: ' + data['text']

        # Time
        slug = job.workspace['created_time']

    else:
        # Notification

        # Email formatting
        email['name'] = "Food Alert Notification"
        subj = "[UW Food Alert] Food Available: {}, {}"
        email['subject'] = subj.format(data['event'], data['location'])
        data['time']['end'] = parser.parse(job.workspace['time_end'])
        email['body'] = Sender.format_message(data)

        # SMS formatting
        sms = email['body']
        # Text message is the same as the body of the email

        # Time
        slug = job.workspace['time_created']

    for ch in [' ', ':', '+']:
        slug = slug.replace(ch, '')

    # Queue up the actual sending of email/sms
    Job.objects.create(name='send_email',
                       workspace={'recipients': email_recipients,
                                  'email': email,
                                  'time': slug})

    Job.objects.create(name='send_sms',
                       workspace={'recipients': sms_recipients,
                                  'sms': sms})


def send_email(job):
    Sender.send_email(job.workspace['email'],
                      job.workspace['recipients'],
                      job.workspace['time'])


def send_sms(job):
    if debug_mode:
        logger.info('Not sending sms while in debug mode')
        logger.info(job.workspace)
    else:
        Sender.send_twilio_sms(job.workspace['recipients'],
                               job.workspace['sms'])
