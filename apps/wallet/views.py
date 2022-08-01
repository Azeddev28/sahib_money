from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model

from apps.banks.models import SahibMoneyBank
from apps.wallet.forms import DepositForm
from apps.wallet.models import DepositTransaction, Transaction

User = get_user_model()


class SelectBankListView(View):
    template_name = 'wallet/select_deposit_bank.html'

    def get(self, request, *args, **kwargs):
        banks = SahibMoneyBank.objects.filter(is_active=True).values('account_no', 'account_name', 'iban_no')
        context = {'banks': banks}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        request.session['user-selected-bank'] = {
            'account_name': request.POST.get('bank_account_name'),
            'account_no': request.POST.get('bank_account_no'),
            'iban_no': request.POST.get('bank_iban_no'),
        }
        return redirect('payment-deposit')


class DepositTransactionView(View):
    template_name = 'wallet/wallet_deposit.html'

    def get(self, request, *args, **kwargs):
        form = DepositForm()
        print(request.session['user-selected-bank'])
        bank = request.session['user-selected-bank']
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


class DepositRequestListView(View):
    template_name = 'wallet/deposit_requests.html'

    def get(self, request, *args, **kwargs):
        context = {
            'transactions': DepositTransaction.objects.filter(wallet__user=request.user).order_by('-created')
        }
        return render(request, self.template_name, context)    
