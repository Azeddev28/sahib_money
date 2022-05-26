import uuid

from django.db import models
from django.contrib.auth import get_user_model

from apps.base_models import TimeStamp
from apps.payments.utils.receipt_files_path import get_receipt_file_path

User = get_user_model()


class Payment(TimeStamp):
    WAITING_FOR_APPROVAL = 0
    APPROVED = 1
    DECLINED = 2

    PAYMENT_STATUS_CHOICES = (
        (WAITING_FOR_APPROVAL, 'Waiting for Approval'),
        (APPROVED, 'Approved'),
        (DECLINED, 'Declined'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payments')
    amount = models.FloatField()
    receipt = models.ImageField(upload_to=get_receipt_file_path)
    status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=WAITING_FOR_APPROVAL)

    def __repr__(self):
        return 'Payment(%s, %s)' % (self.email, self.file)

    def __str__ (self):
        return self.user.email
