import uuid

from django.db import models
from django.contrib.auth import get_user_model

from django_extensions.db.models import TimeStampedModel

from apps.wallet.utils.receipt_files_path import get_receipt_file_path


User = get_user_model()


class Wallet(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_wallet')
    total_amount = models.FloatField()


class Transaction(TimeStampedModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_wallet')
    amount = models.FloatField()


class P2PTransaction(Transaction):
    receiver_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transaction_receiver_wallet')


class BankDetail(models.Model):
    account_no = models.CharField(max_length=30)
    iban_no = models.CharField(max_length=10)
    account_name = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bank_details')


class DepositTransaction(Transaction):
    WAITING_FOR_APPROVAL = 0
    APPROVED = 1
    DECLINED = 2

    PAYMENT_STATUS_CHOICES = (
        (WAITING_FOR_APPROVAL, 'Waiting for Approval'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    )

    receipt = models.ImageField(upload_to=get_receipt_file_path)
    status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=WAITING_FOR_APPROVAL)


class WithdrawalTransaction(Transaction):
    PENDING = 0
    SENT = 1

    PAYMENT_STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (SENT, 'Sent'),
    )

    status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=PENDING)
    bank_details = models.ForeignKey(BankDetail, on_delete=models.SET_NULL, related_name='transaction_bank_details', null=True)
