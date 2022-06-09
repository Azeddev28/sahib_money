from django import forms

from apps.wallet.models import DepositTransaction


class DepositForm(forms.ModelForm):

   class Meta:
      model = DepositTransaction
      exclude = ['wallet', 'status']
