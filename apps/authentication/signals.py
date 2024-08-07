from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from apps.activities.choices import ActivityTypes
from apps.activities.models import Activity

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


@receiver(user_logged_in)
def post_login(sender, user, request, **kwargs):
    Activity.objects.create(
        user=user,
        action=ActivityTypes.LOGIN,
        details=f'Login IP {user.last_client_ip}'
    )
