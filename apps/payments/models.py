from django.db import models
from django.contrib.auth import get_user_model

from apps.base_models import TimeStamp

User = get_user_model()


class Payment(TimeStamp):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_payments')
    amount = models.FloatField()
    receipt = models.ImageField(upload_to='receipts')

    def __repr__(self):
        return 'Payment(%s, %s)' % (self.email, self.file)

    def __str__ (self):
        return self.user.email
