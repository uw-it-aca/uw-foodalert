import time
import logging
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

  # Handle the formatting of messages based on if the message is for a Notifcation or Update
  data = job.workspace['data']
  email = {}
  sms = ''
  slug = ''
  
  if job.workspace['update']:
    # Update

    # Email formatting
    email['name'] = "Food Alert Update"
    email['subject'] = "[UW Food Alert] Update: {}, {}".format(job.workspace['event'], job.workspace['location'])
    email['body'] = ('Update: ' + data['text'] + '\n\n'
                    'Thanks,\n'
                    'UW Food Alert')

    # SMS formatting
    sms = job.workspace['event'] + ' Update: ' + data['text']

    # Time
    slug = str(data['created_time'])
    
  else:
    # Notification

    # Email formatting
    email['name'] = "Food Alert Notification"
    email['subject'] = "[UW Food Alert] Food Available: {}, {}".format(data['event'], data['location'])
    print('HERE')
    print(data)
    email['body'] = Sender.format_message(data)

    # SMS formatting
    sms = email['body'] # Text message is the same as the body of the email

    # Time
    slug = str(data['time']['created'])

  for ch in [' ', ':', '+']:
      slug = slug.replace(ch, '')

  # Queue up the actual sending of email/sms
  Job.objects.create(name='send_email', workspace={'recipients': email_recipients,
                                                   'email': email,
                                                   'time': slug})
  Job.objects.create(name='send_sms', workspace={'recipients': sms_recipients,
                                                 'sms': sms})

def send_email(job):
  if debug_mode:
    logger.info('Not sending emails while in debug mode')
    logger.info(job.workspace)
  else:
    recipients, email, time = job.workspace['recipients'], job.workspace['email'], job.workspace['time']
    Sender.send_email(recipients, email, time)

def send_sms(job):
  if debug_mode:
    logger.info('Not sending sms while in debug mode')
    logger.info(job.workspace)
  else:
    recipients, sms = job.workspace['recipients'], job.workspace['sms']
    Sender.send_twilio_sms(recipients, sms)