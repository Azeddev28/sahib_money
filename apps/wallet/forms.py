from django import forms
from django.contrib.auth import get_user_model

from apps.wallet.models import DepositTransaction, WithdrawalTransaction, P2PTransaction, Wallet
from apps.banks.models import UserBank
from apps.wallet.utils.wallet_utils import get_available_credits

User = get_user_model()


class DepositForm(forms.ModelForm):
   bank_details = forms.ModelChoiceField(
      queryset=UserBank.objects.all(),
      empty_label="--Select Bank Account--",
   )
   class Meta:
      model = DepositTransaction
      exclude = ['wallet', 'status']

   def __init__(self, *args, **kwargs):
      super(DepositForm, self).__init__(*args, **kwargs)
      self.fields['bank_details'].widget.attrs['class'] = 'form-control'



class WithdrawalForm(forms.ModelForm):
   bank_details = forms.ModelChoiceField(
      queryset=UserBank.objects.all(),
      empty_label="--Select Bank Account--",
      required=True
   )
   class Meta:
      model = WithdrawalTransaction
      exclude = ['wallet', 'status']

   def __init__(self, *args, **kwargs):
      self.request = kwargs.pop('request', None)
      super(WithdrawalForm, self).__init__(*args, **kwargs)
      self.fields['bank_details'].widget.attrs['class'] = 'form-control'


   def clean_amount(self):
      requested_credits = self.cleaned_data.get("amount")
      available_credits = get_available_credits(self.request.user)
      if available_credits < requested_credits:
         raise forms.ValidationError(
            "Your requested credits exceed the available credits."
         )

      return requested_credits


class WalletTransferForm(forms.ModelForm):
   email = forms.EmailField()
   class Meta:
      model = P2PTransaction
      exclude = ['wallet', 'status', 'to_wallet']

   def __init__(self, *args, **kwargs):
      self.request = kwargs.pop('request', None)
      super(WalletTransferForm, self).__init__(*args, **kwargs)

   def clean_email(self):
      email = self.cleaned_data.get("email")
      try:
         user = User.objects.get(email=email)
         wallet = user.wallet
         if self.request.user == user:
            raise forms.ValidationError(
               "Please enter receiver email"
            )
      except User.DoesNotExist:
         raise forms.ValidationError(
            "User does not exist with this email"
         )
      except Wallet.DoesNotExist:
         raise forms.ValidationError(
            "Wallet does not exist with this email"
         )
      return email
