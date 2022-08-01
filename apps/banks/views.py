from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.conf import settings

from apps.banks.forms import UserBankForm


class UserBankView(View):
    template_name = 'banks/user_bank_details.html'

    def get(self, request, *args, **kwargs):
        form = UserBankForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = UserBankForm(request.POST)
        if form.is_valid():
            bank_details = form.save(commit=False)
            bank_details.user = request.user
            bank_details.save()

            form = UserBankForm()
            context = {
                'form': form,
                'form_success': True
            }
            return render(request, self.template_name, context)
        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        context = {'form': form}
        return render(request, self.template_name, context)
