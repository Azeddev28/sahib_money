from django import forms

from apps.banks.models import UserBank

class UserBankForm(forms.ModelForm):
    class Meta:
        model = UserBank
        exclude = ['user', 'is_active']
