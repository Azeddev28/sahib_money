from django.conf import settings
from django.core.mail import send_mail


class EmailService:
    def __init__(self, subject, message, recipients):
        self.subject = subject
        self.email_from = settings.EMAIL_HOST_USER
        self.message = message
        self.recipients = recipients

    def send_email(self):
        is_email_sent = send_mail(self.subject, self.message,
                                  self.email_from, self.recipients)
        return is_email_sent
