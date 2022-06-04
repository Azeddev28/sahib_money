from django.db import models
from django_extensions.db.models import TimeStampedModel
from django.contrib.auth import get_user_model
from hashid_field import BigHashidAutoField

from apps.wallet.models import Transaction

User = get_user_model()


class MerchantAccount(TimeStampedModel):
    account_name = models.CharField(max_length=40, null=False, blank=False)
    merchant_secret_key = BigHashidAutoField(primary_key=True, min_length=20)
    account_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='merchant_account_user')


class ThirdPartyTransaction(Transaction):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    PENDING = 0
    SENT = 1

    TRANSACTION_TYPE_CHOICES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw')
    )

    PAYMENT_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
    )

    merchant_account = models.OneToOneField(MerchantAccount, on_delete=models.CASCADE, related_name='transaction_merchant')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)
    status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=PENDING)
