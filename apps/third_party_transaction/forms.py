from django import forms
from .models import TransactionOTP


class OTPForm(forms.Form):
    otp = forms.CharField(required=True)

