from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.authentication.services.email_verification import EmailVerificationService

User = get_user_model()

@receiver(post_save, sender=User)
def send_verification_email(sender, instance, created, **kwargs):
    if created:
        email_service = EmailVerificationService(instance.email, instance.uuid)
        email_service.send_email()
