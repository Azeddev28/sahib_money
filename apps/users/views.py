from django.shortcuts import render
from django.views import View


class ProfileDetailsView(View):
    user_profile_template = 'users/profile.html'
    merchant_profile_template = 'users/merchant_profile.html'

    def get(self, request, *args, **kwargs):
        if getattr(request.user, 'merchant_account', None):
            return render(request, self.merchant_profile_template, {})

        return render(request, self.user_profile_template, {})
