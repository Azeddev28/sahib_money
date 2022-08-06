from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy

from .forms import MerchantAccountForm
from .models import MerchantAccount


class ProfileDetailsView(View):
    user_profile_template = 'users/user_profile.html'
    merchant_profile_template = 'users/merchant_user_profile.html'

    def get(self, request, *args, **kwargs):
        if getattr(request.user, 'merchant_account', None):
            merchant = MerchantAccount.objects.get(user=request.user.id)
            form = MerchantAccountForm(instance=merchant)
            return render(request, self.merchant_profile_template, {'form': form})

        return render(request, self.user_profile_template, {})

    def post(self, request, *args, **kwargs):
        merchant = MerchantAccount.objects.get(user=request.user.id)
        form = MerchantAccountForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            form = MerchantAccountForm(instance=merchant)
            return render(request, self.merchant_profile_template, {'form': form})


class ResetPassword(SuccessMessageMixin, PasswordResetView):
    template_name = 'home/page_forgot_password.html'
    email_template_name = 'home/password_reset_email.html'
    subject_template_name = 'home/password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login')


class APIDetailsView(View):
    merchant_profile_template = 'users/api_settings.html'

    def get(self, request, *args, **kwargs):
        if getattr(request.user, 'merchant_account', None):
            merchant = MerchantAccount.objects.get(user=request.user.id)
            form = MerchantAccountForm(instance=merchant)
            return render(request, self.merchant_profile_template, {'form': form})

        return render(request, self.user_profile_template, {})
