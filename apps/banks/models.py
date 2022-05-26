from django.db import models

from apps.base_models import BaseModel


class Bank(BaseModel):
    account_name = models.CharField(max_length=200)
    account_no = models.CharField(max_length=200)
    iban = models.CharField(max_length=200)

    def __str__(self):
        return self.account_name    