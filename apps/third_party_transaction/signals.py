from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.services.email_service import EmailService
from apps.third_party_transaction.models import TransactionOTP, ThirdPartyTransaction
from apps.wallet.choices import PaymentStatus
from apps.wallet.services.wallet_transaction import WalletTransactionService


@receiver(post_save, sender=ThirdPartyTransaction)
def deduct_amount_after_approval(sender, instance:ThirdPartyTransaction, created, **kwargs):
    if not created:
        if instance.payment_status == PaymentStatus.APPROVED:
            WalletTransactionService.deduct_amount(instance.wallet, instance.amount)


@receiver(post_save, sender=TransactionOTP)
def send_otp_verification_email(sender, instance, created, **kwargs):
    if created:
        email_service = EmailService(
            'Sahib Money OTP Verification',
            [instance.transaction.wallet.user.email,],
            'email_templates/otp_email.html',
            {
                'verification_code': instance.otp_code
            }
        )
        email_service.start()
