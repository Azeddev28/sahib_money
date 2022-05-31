from django.shortcuts import render
from django.views import View
from django.contrib import messages
from apps.banks.models import Bank
from apps.wallet.models import Wallet, WalletTransaction
from apps.wallet.services.wallet_service import WalletTransactionService
from apps.payments.forms import PaymentForm, WithdrawalForm


class DepositPaymentView(View):
    def get(self, request, *args, **kwargs):
        form = PaymentForm
        bank = Bank.objects.filter(is_active=True).first()
        context = {'form': form, 'bank': bank}
        return render(request, 'payments/upload.html', context)

    def post(self, request, *args, **kwargs):
        bank = Bank.objects.filter(is_active=True).first()
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()
            user_wallet, created = Wallet.objects.get_or_create(user=request.user)
            WalletTransactionService().perform_user_account_deposit(user_wallet,
                                                                      amount=float(form['amount'].value()),
                                                                      account_no=None)
            form = PaymentForm
            context = {
                'form': form, 
                'bank': bank,
                'form_success': True
            }
            return render(request, 'payments/upload.html', context)

        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        form = PaymentForm
        context = {'form': form, 'bank': bank}
        return render(request, 'payments/upload.html', context)

class WithdrawPaymentView(View):
    def get(self, request, *args, **kwargs):
        form = WithdrawalForm
        return render(request, 'payments/withdraw.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = WithdrawalForm(request.POST, request.FILES)
        if form.is_valid():
            user_wallet, created = Wallet.objects.get_or_create(user=request.user)
            is_succeeded = WalletTransactionService().perform_user_account_withdrawl(user_wallet,
                                                                      amount=float(form['amount'].value()),
                                                                      account_no=form['account_no'].value())
            
            form = WithdrawalForm
            context = {
                'form': form,
                'form_success': True
            }
            return render(request, 'payments/withdraw.html', context)

            if is_succeeded is not True:
                messages.error(request, 'Insufficient credits')

        messages.error(request, 'Invalid form submission.')
        messages.error(request, form.errors)
        form = WithdrawalForm
        context = {'form': form}
        return render(request, 'payments/withdraw.html', context)

