from django.conf import settings
from django.urls import reverse

from apps.services.email_service import EmailService
from apps.authentication.utils.constants import VERIFY_ACCOUNT


class EmailVerificationService(EmailService):
    def __init__(self, recipient_email, user_uuid):
        self.user_uuid = user_uuid
        subject = VERIFY_ACCOUNT
        message = self.get_email_body()
        recipients = [recipient_email]
        super().__init__(subject, message, recipients)

    def get_email_body(self):
        return f"""Follow the link to verify account
        {settings.SITE_BASE_URL}{reverse('verify-account', args=(self.user_uuid,))}
        """
