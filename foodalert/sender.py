from dbmail import send_db_mail
from dbmail.models import MailTemplate
from django.conf import settings


class Sender:

    def send_email(body, recipients):
        MailTemplate.objects.create(
            name="Food Alert!",
            subject="New Hungry Husky Event is Open",
            message=body,
            slug="message",
            is_html=False,
        )

        send_db_mail(
            slug='message',
            recipient=settings.SAFE_EMAIL_RECIPIENT,
            bcc=recipients,
            use_celery=False
        )
