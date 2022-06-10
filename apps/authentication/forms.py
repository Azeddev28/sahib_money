from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from apps.users.models import MerchantAccount

User = get_user_model()


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class MerchantSignUpForm(forms.ModelForm):
    company_website = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Company Website",
                "class": "form-control"
            }
        ))
    merchant_account_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Business Name",
                "class": "form-control"
            }
        ))

    class Meta:
        model = MerchantAccount
        fields = ('company_website', 'merchant_account_name')
