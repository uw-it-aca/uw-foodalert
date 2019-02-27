from dbmail import send_db_mail
from dbmail.models import send_db_mail


class Sender:

    def send_email(body, recipients):
        MailTemplate.objects.create(
            name="Food Alert!",
            subject="Test",
            message=body,
            slug="message",
            is_html=False,
        )

        send_db_mail('message', recipients, use_celery=False)
