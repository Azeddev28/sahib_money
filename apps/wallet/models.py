import uuid

from django.db import models
from django.contrib.auth import get_user_model

from apps.base_models import TimeStamp

User = get_user_model()


class Wallet(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_wallet')
    total_amount = models.FloatField()


class WalletTransaction(TimeStamp):
    DEPOSIT = 0
    WITHDRAW = 1

    TRANSACTION_TYPE_CHOICES = (
        (DEPOSIT, 'Deposit'),
        (WITHDRAW, 'Withdraw')
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    from_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_from_wallet')
    to_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_to_wallet')
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE_CHOICES)
    amount = models.FloatField()
