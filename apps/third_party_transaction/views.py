from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.third_party_transaction.models import ThirdPartyTransaction, TransactionOTP
from apps.wallet.choices import TransactionStatus
from .forms import OTPForm

class OTPView(View, LoginRequiredMixin):
    def get(self, request, uuid, *args, **kwargs):
        if request.user != transaction.wallet.user:
            return render(request, 'third_party_transaction/errors.html', {'errors': "Invalid user"})

        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return render(request, 'third_party_transaction/errors.html', {'errors': "Transaction does not exist"})

        if transaction.is_invalid():
            return render(request, 'third_party_transaction/errors.html', {'errors': "Transaction is not valid anymore"})

        transaction_otp = transaction.otps.order_by('-created').first()
        if not transaction_otp or transaction_otp.has_expired():
           TransactionOTP.objects.create(transaction=transaction)
        # user ko email men bhej do aync task men
        return render(request, 'third_party_transaction/otp.html', {'form': OTPForm(), 'uuid': uuid})


    def post(self, request, *args, **kwargs):
        otp = request.POST.get('otp')
        uuid = str(kwargs.get('uuid'))
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            context = {'errors': "Transaction does not exist"}
            return render(request, 'third_party_transaction/errors.html', context)

        transaction_otp = transaction.otps.order_by('-created').first()
        if transaction_otp and str(transaction_otp) == otp:
            transaction.status = TransactionStatus.VERIFIED
            transaction.otps.all().delete()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            context = {'errors': "Invalid OTP"}
            return render(request, 'third_party_transaction/errors.html', context)
