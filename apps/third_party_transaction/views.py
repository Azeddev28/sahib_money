from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.services.email_service import EmailService

from apps.third_party_transaction.models import ThirdPartyTransaction, TransactionOTP
from apps.wallet.choices import TransactionStatus


class OTPView(LoginRequiredMixin, View):
    def get(self, request, uuid, *args, **kwargs):
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return render(request, 'third_party_transaction/errors.html', {'error': "Transaction does not exist"})

        if request.user != transaction.wallet.user:
            return render(request, 'third_party_transaction/errors.html', {'error': "Invalid user"})

        if transaction.is_invalid():
            return render(request, 'third_party_transaction/errors.html', {'error': "Transaction is not valid anymore"})

        try:
            transaction_otp = transaction.otp
        except TransactionOTP.DoesNotExist:
            TransactionOTP.objects.create(transaction=transaction)

        context = {
            'uuid': uuid,
            'amount': transaction.amount,
            'requested_form': transaction.merchant_account.merchant_account_name,
            'company_website': transaction.merchant_account.company_website
        }
        return render(request, 'third_party_transaction/otp.html', context)


    def post(self, request, uuid, *args, **kwargs):
        otp = request.POST.get('otp')
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return JsonResponse({'error': "Transaction does not exist"}, status=400)

        if transaction.is_invalid():
            return JsonResponse({'error': "Transaction is not valid anymore"}, status=400)

        if transaction.otp.has_expired:
            return JsonResponse({'error': "Transaction otp has expired"}, status=400)

        if transaction.otp and str(transaction.otp.otp_code) == otp:
            transaction.status = TransactionStatus.VERIFIED
            transaction.save()
            transaction.otp.delete()
            context = {
                'success': "Transaction Verified",
                'success_url': transaction.merchant_account.company_website
            }
            return JsonResponse(context, status=200)
        else:
            return JsonResponse({'error': "Invalid OTP"}, status=400)
