from datetime import datetime, timezone
from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth import get_user_model
from hashid_field import HashidAutoField
from apps.users.models import MerchantAccount

from apps.wallet.models import Transaction
from apps.wallet.choices import PaymentStatus, TransactionType, TransactionStatus

User = get_user_model()

class ThirdPartyTransaction(Transaction):
    merchant_account = models.ForeignKey(MerchantAccount, on_delete=models.CASCADE, related_name='merchant_transactions')
    type = models.IntegerField(choices=TransactionType.CHOICES, null=False, blank=False)
    status = models.IntegerField(choices=TransactionStatus.CHOICES, default=TransactionStatus.UNVERIFIED)
    payment_status = models.IntegerField(choices=PaymentStatus.CHOICES, default=PaymentStatus.WAITING_FOR_APPROVAL)

    @property
    def has_expired(self):
        return (datetime.now(timezone.utc) - self.created).total_seconds() > settings.TP_TRANSACTION_TIMEOUT

    def is_invalid(self):
        return self.has_expired or self.status in [TransactionStatus.CANCELLED, TransactionStatus.VERIFIED]


class TransactionOTP(TimeStampedModel):
    otp_code = HashidAutoField(primary_key=True, min_length=15)
    transaction = models.OneToOneField(ThirdPartyTransaction, on_delete=models.CASCADE, related_name='otp')

    @property
    def has_expired(self):
        return (datetime.now(timezone.utc) - self.created).total_seconds() > settings.OTP_TIMEOUT
