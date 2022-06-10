from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from apps.wallet.choices import PaymentStatus

from apps.wallet.utils.email_utils import send_approval_email_to_user, send_refusal_email_to_user, send_payment_request_email_to_admin
from apps.wallet.models import DepositTransaction
from apps.wallet.services.wallet_transaction import WalletTransactionService
from apps.wallet.models import Wallet

User = get_user_model()


@receiver(pre_save, sender=DepositTransaction)
def handle_payment_status_update(sender, instance: DepositTransaction, **kwargs):
    if not instance._state.adding:
        prev_instance = DepositTransaction.objects.get(pk=instance.pk)
        user_name = f'{instance.wallet.user.first_name or ""} {instance.wallet.user.last_name or ""}'
        email = instance.wallet.user.email

        if prev_instance.status != PaymentStatus.APPROVED and\
            instance.status == PaymentStatus.APPROVED:
            send_approval_email_to_user(user_name, email)
            WalletTransactionService.deposit_amount(instance.wallet, instance.amount)
        if prev_instance.status != PaymentStatus.DECLINED and\
            instance.status == PaymentStatus.DECLINED:
            send_refusal_email_to_user(user_name, email)


@receiver(post_save, sender=DepositTransaction)
def send_admin_payment_request(sender, instance, created, **kwargs):
    if created:
        instance_url = settings.SITE_BASE_URL + f'/admin/wallet/deposittransaction/{instance.pk}/change/'
        send_payment_request_email_to_admin(instance_url)


@receiver(post_save, sender=User)
def create_wallet_on_registration(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)
