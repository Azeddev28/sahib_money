from django import forms
from .models import Payment
from apps.wallet.models import WalletTransaction


class PaymentForm(forms.ModelForm):

   class Meta:
      model = Payment
      exclude = ['user', 'status']


class WithdrawalForm(forms.ModelForm):

   class Meta:
      model = WalletTransaction
      fields = ['amount', 'account_no']

