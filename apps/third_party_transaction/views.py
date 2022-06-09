from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.third_party_transaction.models import ThirdPartyTransaction, TransactionOTP
from apps.wallet.choices import TransactionStatus


class OTPView(LoginRequiredMixin, View):
    login_url = '/login/'
    def get(self, request, uuid, *args, **kwargs):
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return render(request, 'third_party_transaction/errors.html', {'errors': "Transaction does not exist"})

        if request.user != transaction.wallet.user:
            return render(request, 'third_party_transaction/errors.html', {'errors': "Invalid user"})

        if transaction.is_invalid():
            return render(request, 'third_party_transaction/errors.html', {'errors': "Transaction is not valid anymore"})

        try:
            transaction_otp = transaction.otp
        except TransactionOTP.DoesNotExist:
            TransactionOTP.objects.create(transaction=transaction)
        # user ko email men bhej do aync task men
        return render(request, 'third_party_transaction/otp.html', {'uuid': uuid})


    def post(self, request, uuid, *args, **kwargs):
        otp = request.POST.get('otp')
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            context = {'errors': "Transaction does not exist"}
            return JsonResponse(context, status=400)

        if transaction.is_invalid():
            context = {'errors': "Transaction is not valid anymore"}
            return JsonResponse(context, status=400)

        if transaction.otp.has_expired:
            context = {'errors': "Transaction otp has expired"}
            return JsonResponse(context, status=400)

        if transaction.otp and str(transaction.otp.otp_code) == otp:
            transaction.status = TransactionStatus.VERIFIED
            transaction.save()
            transaction.otp.delete()
            context = {
                'success': "Transaction Verified",
                'success_url': "/"
            }
            return JsonResponse(context, status=200)
        else:
            context = {'errors': "Invalid OTP"}
            return JsonResponse(context, status=400)
