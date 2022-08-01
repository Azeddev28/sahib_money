from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.conf import settings

from apps.banks.models import SahibMoneyBank, UserBank
from apps.wallet.choices import TransactionType
from apps.wallet.forms import DepositForm, WithdrawalForm, WalletTransferForm
from apps.wallet.models import DepositTransaction, WithdrawalTransaction, Transaction, Wallet
from apps.wallet.utils.wallet_utils import get_available_credits

User = get_user_model()


class DepositTransactionView(View):
    template_name = 'wallet/wallet_deposit.html'

    def get(self, request, *args, **kwargs):
        form = DepositForm()
        form.fields['bank_details'].queryset = UserBank.objects.filter(user=request.user)
        bank = SahibMoneyBank.objects.filter(is_active=True).first()
        context = {'form': form, 'bank': bank}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        bank = SahibMoneyBank.objects.filter(is_active=True).first()
        form = DepositForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.wallet = request.user.wallet
            transaction.save()
            form = DepositForm()
            form.fields['bank_details'].queryset = UserBank.objects.filter(user=request.user)
            context = {
                'form': form,
                'bank': bank,
                'form_success': True
            }
            return render(request, self.template_name, context)

        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        form.fields['bank_details'].queryset = UserBank.objects.filter(user=request.user)
        context = {'form': form, 'bank': bank}
        return render(request, self.template_name, context)


class TransactionListView(View):
    template_name = 'wallet/transaction_history.html'

    def get(self, request, *args, **kwargs):
        context = {
            'transactions': Transaction.objects.filter(wallet__user=request.user).order_by('-created')
        }
        return render(request, self.template_name, context)


class DepositRequestListView(View):
    template_name = 'wallet/deposit_requests.html'

    def get(self, request, *args, **kwargs):
        context = {
            'transactions': DepositTransaction.objects.filter(wallet__user=request.user).order_by('-created')
        }
        return render(request, self.template_name, context)


class WithdrawalTransactionView(View):
    template_name = 'wallet/wallet_withdraw.html'

    def get(self, request, *args, **kwargs):
        form = WithdrawalForm()
        form.fields['bank_details'].queryset = UserBank.objects.filter(user=request.user)
        context = {'form': form, 'available_credits': get_available_credits(self.request.user)}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = WithdrawalForm(request.POST, request=request)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.wallet = request.user.wallet
            transaction.save()

            form = WithdrawalForm()
            form.fields['bank_details'].queryset = UserBank.objects.filter(user=request.user)
            context = {
                'form': form,
                'form_success': True,
                'available_credits': get_available_credits(self.request.user)
            }
            return render(request, self.template_name, context)

        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        form.fields['bank_details'].queryset = UserBank.objects.filter(user=request.user)
        context = {'form': form, 'available_credits': get_available_credits(self.request.user)}
        return render(request, self.template_name, context)


class WithdrawRequestListView(View):
    template_name = 'wallet/withdraw_requests.html'

    def get(self, request, *args, **kwargs):
        context = {
            'transactions': WithdrawalTransaction.objects.filter(wallet__user=request.user).order_by('-created')
        }
        return render(request, self.template_name, context)


class P2PTransactionView(View):
    template_name = 'wallet/wallet_transfer.html'

    def get(self, request, *args, **kwargs):
        form = WalletTransferForm()
        context = {'form': form, 'available_credits': get_available_credits(self.request.user)}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = WalletTransferForm(request.POST, request=request)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.wallet = request.user.wallet
            receiver = User.objects.get(email=form.cleaned_data.get('email'))
            transaction.to_wallet = receiver.wallet
            transaction.save()

            form = WalletTransferForm()
            context = {
                'form': form,
                'form_success': True,
                'available_credits': get_available_credits(self.request.user)
            }
            return render(request, self.template_name, context)

        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        context = {'form': form, 'available_credits': get_available_credits(self.request.user)}
        return render(request, self.template_name, context)
