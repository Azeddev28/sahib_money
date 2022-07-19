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
            'transactions': Transaction.objects.filter(wallet__user=request.user)
        }
        return render(request, self.template_name, context)    

class WalletTransactionView(View):
    template_name = 'wallet/wallet_iframe.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        requested_credits = request.POST.get('amount')
        user_email = request.POST.get('email')

        print(requested_credits)
        print(user_email)

        user = None
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            pass
            # return Response({'error': "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # check if another third party transaction is in pipeline from the same user
        try:
            last_transaction = user.wallet.transactions\
                                .select_related('thirdpartytransaction')\
                                .order_by('-created')\
                                .first()
        except Wallet.DoesNotExist:
            pass
            # return Response({'error': "User wallet does not exist"} ,status=status.HTTP_400_BAD_REQUEST)

        if last_transaction:
            last_transaction = ThirdPartyTransaction.objects.get(uuid=last_transaction.uuid)
            if not last_transaction.is_invalid():
                pass
                # return Response({'error': "Another transaction is in progress"}, status=status.HTTP_400_BAD_REQUEST)

        # check if requested withdrawal credits are greater than available credits in user wallet
        if requested_credits > user.wallet.total_amount:
            pass
            # return Response({'error': "User does not have enough credits in the wallet"}, status=status.HTTP_400_BAD_REQUEST)

        transaction_reference = request.POST.get('transaction_reference', '')
        try:
            # create third party withdraw transaction
            transaction = ThirdPartyTransaction.objects.create(
                wallet=user.wallet,
                reference=transaction_reference,
                merchant_account=request.user.merchant_account,
                type=TransactionType.THIRD_PARTY_WITHDRAW,
                amount=requested_credits
            )
        except IntegrityError:
            pass
            # return Response({'error': "This transaction reference has already been used"}, status=status.HTTP_400_BAD_REQUEST)

        # Changing this part to return otp url
        return redirect(f"{settings.SITE_BASE_URL}{reverse('otp_view', args=(transaction.uuid,))}")
