from django.db import models
from django.contrib.auth import get_user_model

from apps.base_models import TimeStamp

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payments')
    amount = models.FloatField()
    receipt = models.ImageField(upload_to='receipts')
    status = models.IntegerField(choices=PAYMENT_STATUS_CHOICES, default=WAITING_FOR_APPROVAL)

    def __repr__(self):
        return 'Payment(%s, %s)' % (self.email, self.file)

    def __str__ (self):
        return self.user.email
