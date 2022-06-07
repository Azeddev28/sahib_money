import uuid

from django.db import models
from django.contrib.auth import get_user_model

from django_extensions.db.models import TimeStampedModel

from apps.wallet.utils.receipt_files_path import get_receipt_file_path
from apps.wallet.choices import PaymentStatus

User = get_user_model()


class Wallet(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    total_amount = models.FloatField(default=0)


class Transaction(TimeStampedModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField()


class P2PTransaction(Transaction):
    to_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions_to_wallet')


class BankDetail(models.Model):
    account_no = models.CharField(max_length=64)
    iban_no = models.CharField(max_length=64)
    account_name = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bank_details')


class DepositTransaction(Transaction):
    receipt = models.ImageField(upload_to=get_receipt_file_path)
    status = models.IntegerField(choices=PaymentStatus.CHOICES, default=PaymentStatus.WAITING_FOR_APPROVAL)


class WithdrawalTransaction(Transaction):
    bank_details = models.ForeignKey(BankDetail, on_delete=models.SET_NULL, related_name='transaction_bank_details', null=True)
    status = models.IntegerField(choices=PaymentStatus.CHOICES, default=PaymentStatus.WAITING_FOR_APPROVAL)
