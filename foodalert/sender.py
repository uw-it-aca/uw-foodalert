from dbmail import send_db_mail
from dbmail.models import MailTemplate
from django.conf import settings


class Sender:
    def send_email(body, recipients, time):
        if body[:6] == 'Update':
            print('making update with ' + time)
            MailTemplate.objects.create(
                name="Food Alert Update",
                subject="A Hungry Husky Event has posted an update",
                message=body,
                slug=time,
                is_html=False,
            )
        else:
            print('making notif with ' + time)
            MailTemplate.objects.create(
                name="Food Alert Notification",
                subject="New Hungry Husky Event is Open",
                message=body,
                slug=time,
                is_html=False,
            )

        send_db_mail(
            slug=time,
            recipient=settings.SAFE_EMAIL_RECIPIENT,
            bcc=recipients,
            use_celery=False
        )
