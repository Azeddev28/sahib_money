from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.conf import settings

from apps.banks.models import SahibMoneyBank
from apps.third_party_transaction.models import ThirdPartyTransaction
from apps.wallet.choices import TransactionType
from apps.wallet.forms import DepositForm
from apps.wallet.models import Transaction, Wallet

User = get_user_model()


class DepositTransactionView(View):
    template_name = 'wallet/wallet_deposit.html'

    def get(self, request, *args, **kwargs):
        form = DepositForm()
        bank = SahibMoneyBank.objects.filter(is_active=True).first()
        context = {'form': form, 'bank': bank}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        bank = SahibMoneyBank.objects.filter(is_active=True).first()
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.wallet = request.user.wallet
            payment.save()

            form = DepositForm()
            context = {
                'form': form,
                'bank': bank,
                'form_success': True
            }
            return render(request, self.template_name, context)

        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        form = DepositForm()
        context = {'form': form, 'bank': bank}
        return render(request, self.template_name, context)


class TransactionListView(View):
    template_name = 'wallet/transaction_history.html'

    def get(self, request, *args, **kwargs):
        context = {
            'transactions': Transaction.objects.filter(wallet__user=request.user).order_by('-created')
        }
        return render(request, self.template_name, context)    
