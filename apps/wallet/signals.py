from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from apps.wallet.models import Wallet, WalletTransaction
from apps.payments.utils.email_utils import send_withdrawal_email_to_user


@receiver(pre_save, sender=Wallet)
def send_withdrawal_status_email(sender, instance, **kwargs):
    prev_instance = Wallet.objects.get(pk=instance.pk)
    user_name = f'{instance.user.first_name or ""} {instance.user.last_name or ""}'
    email = instance.user.email

    if prev_instance.total_amount > instance.total_amount:
        amount_diff = prev_instance.total_amount - instance.total_amount
        send_withdrawal_email_to_user(user_name, email, amount_diff, instance.total_amount)
