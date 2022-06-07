from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.third_party_transaction.models import ThirdPartyTransaction, TransactionOTP
from .forms import OTPForm

class OTPView(View, LoginRequiredMixin):
    def get(self, request, uuid, *args, **kwargs):
        user = request.user
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            context = {'errors': "Transaction DoesNotExist"}
            return render(request, 'third_party_transaction/errors.html', context)
    
        if user != transaction.wallet.user:
            context = {'errors': "Invalid user"}
            return render(request, 'third_party_transaction/errors.html', context)

        otp = TransactionOTP.objects.create(transaction=transaction)
        context = {
            'form': OTPForm(),
            'transaction_uuid': uuid
        }
        # user ko email men bhej do aync task men
        return render(request, 'third_party_transaction/otp.html', context)


    def post(self, request, *args, **kwargs):
        otp = request.POST.get('otp')
        uuid = str(kwargs.get('uuid'))
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            context = {'errors': "Transaction DoesNotExist"}
            return render(request, 'third_party_transaction/errors.html', context)

        if otp == str(transaction.otps.order_by('-created').first().otp):
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            context = {'errors': "Invalid OTP"}
            return render(request, 'third_party_transaction/errors.html', context)
