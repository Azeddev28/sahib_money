from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.payments.models import Payment
from apps.payments.utils.email_utils import send_approval_email_to_user, send_refusal_email_to_user


@receiver(pre_save, sender=Payment)
def send_payment_status_email(sender, instance, **kwargs):
    if not instance._state.adding:
        prev_instance = Payment.objects.get(pk=instance.pk)
        user_name = f'{instance.user.first_name or ""} {instance.user.last_name or ""}'
        email = instance.user.email

        if prev_instance.status != Payment.APPROVED and\
            instance.status == Payment.APPROVED:
            send_approval_email_to_user(user_name, email)
        if prev_instance.status != Payment.DECLINED and\
            instance.status == Payment.DECLINED:
            send_refusal_email_to_user(user_name, email)
