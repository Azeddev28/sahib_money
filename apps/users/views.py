from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView
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


class ResetPassword(PasswordResetView):
    template_name = 'home/page_forgot_password.html'
    success_message = '''We've emailed you instructions for setting your password,
                      if an account exists with the email you entered. You should receive them shortly.'''
    success_url = reverse_lazy('reset-password')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['form'].is_valid():
            context['success_message'] = self.success_message
        return context

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return self.render_to_response(self.get_context_data(form=form))


class APIDetailsView(View):
    merchant_profile_template = 'users/api_settings.html'

    def get(self, request, *args, **kwargs):
        if getattr(request.user, 'merchant_account', None):
            merchant = MerchantAccount.objects.get(user=request.user.id)
            form = MerchantAccountForm(instance=merchant)
            return render(request, self.merchant_profile_template, {'form': form})

        return render(request, self.user_profile_template, {})
