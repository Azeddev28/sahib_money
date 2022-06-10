from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings

from apps.services.email_service import EmailService
from apps.authentication.utils.constants import VERIFY_ACCOUNT

User = get_user_model()


@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        email_context = {
            'verification_link': f"{settings.SITE_BASE_URL}{reverse('verify-account', args=(instance.uuid,))}"
        }
        email_service = EmailService(
            subject=VERIFY_ACCOUNT,
            recipients=[instance.email],
            html_template='email_templates/auth_email.html',
            template_context=email_context,
        )
        email_service.start()
