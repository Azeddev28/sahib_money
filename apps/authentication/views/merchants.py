from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate

from apps.authentication.forms import MerchantSignUpForm, SignUpForm


class MerchantRegisterView(View):
    template_name = 'authentication/merchant_register.html'

    def get(self, request, *args, **kwargs):
        signup_form = SignUpForm()
        merchant_form = MerchantSignUpForm()
        context = {
            "merchant_form": merchant_form,
            'signup_form': signup_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        success = None
        msg = None
        merchant_form = MerchantSignUpForm(request.POST)
        signup_form = SignUpForm(request.POST)
        if merchant_form.is_valid() and signup_form.is_valid():
            user = signup_form.save(commit=False)
            email = signup_form.cleaned_data.get("email")
            raw_password = signup_form.cleaned_data.get("password1")
            authenticate(email=email, password=raw_password)
            user.is_active = False
            user.save()

            merchant = merchant_form.save(commit=False)
            merchant.user = user
            merchant.save()
            msg = 'Merchant Account created - please <a href="/login">login</a>.'
            success = True

        else:
            msg = 'Form is not valid'

        context = {
            "merchant_form": merchant_form,
            'signup_form': signup_form,
            "msg": msg,
            "success": success
        }
        return render(request, self.template_name, context)
