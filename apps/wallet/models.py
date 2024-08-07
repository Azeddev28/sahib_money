import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.banks.models import UserBank
from apps.base_models import BaseModel

from django_extensions.db.models import TimeStampedModel

from apps.wallet.utils.receipt_files_path import get_receipt_file_path
from apps.wallet.choices import PaymentStatus

User = get_user_model()


class Wallet(BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    total_amount = models.FloatField(default=0)

    def __str__(self):
        return self.user.email

class Transaction(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField()


class P2PTransaction(Transaction):
    to_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions_to_wallet')


class DepositTransaction(Transaction):
    bank_details = models.ForeignKey(UserBank, on_delete=models.SET_NULL, related_name='deposit_transations', null=True)
    receipt = models.ImageField(upload_to=get_receipt_file_path)
    status = models.IntegerField(choices=PaymentStatus.CHOICES, default=PaymentStatus.WAITING_FOR_APPROVAL)

    @property
    def get_receipt_url(self):
        return f"{settings.MEDIA_URL}/{self.receipt}"
class WithdrawalTransaction(Transaction):
    bank_details = models.ForeignKey(UserBank, on_delete=models.SET_NULL, related_name='withdrawal_transactions', null=True)
    status = models.IntegerField(choices=PaymentStatus.CHOICES, default=PaymentStatus.WAITING_FOR_APPROVAL)
