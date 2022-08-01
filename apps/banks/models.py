from django.db import models
from django.contrib.auth import get_user_model

from apps.base_models import BaseModel

User = get_user_model()


class SahibMoneyBank(BaseModel):
    account_no = models.CharField(max_length=30)
    iban_no = models.CharField(max_length=50)
    account_name = models.CharField(max_length=50)

    def __str__(self):
        return self.account_no

class UserBank(SahibMoneyBank):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_bank_details')
