from django.shortcuts import render
from django.views import View
from django.http import HttpResponseRedirect

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


class ResetPassword(View):
    template_name = 'home/page_forgot_password.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class APIDetailsView(View):
    merchant_profile_template = 'users/api_settings.html'

    def get(self, request, *args, **kwargs):
        if getattr(request.user, 'merchant_account', None):
            merchant = MerchantAccount.objects.get(user=request.user.id)
            form = MerchantAccountForm(instance=merchant)
            return render(request, self.merchant_profile_template, {'form': form})

        return render(request, self.user_profile_template, {})
