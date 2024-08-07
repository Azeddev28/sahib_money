from django.db import models
from django.contrib.auth import get_user_model

from apps.base_models import BaseModel

User = get_user_model()


class SahibMoneyBank(BaseModel):
    class Meta:
        unique_together = ('bank_name', 'account_number')

    bank_name = models.CharField(max_length=64)
    account_name = models.CharField(max_length=64)
    account_number = models.CharField(max_length=64)
    iban_number = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return f"{self.bank_name}:{self.account_name}:{self.account_number}"

class UserBank(SahibMoneyBank):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bank_details')
