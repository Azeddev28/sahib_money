from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse, HttpResponseNotFound
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.third_party_transaction.models import ThirdPartyTransaction, TransactionOTP
from apps.wallet.choices import TransactionStatus


class OTPView(LoginRequiredMixin, View):
    def get(self, request, uuid, *args, **kwargs):
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=uuid)
        except ThirdPartyTransaction.DoesNotExist:
            return HttpResponseNotFound()

        if request.user != transaction.wallet.user:
            return HttpResponseNotFound()

        if transaction.is_invalid():
            return HttpResponseNotFound()

        try:
            transaction_otp = transaction.otp
        except TransactionOTP.DoesNotExist:
            transaction_otp = TransactionOTP.objects.create(transaction=transaction)

        otp_remaining_seconds = round(transaction_otp.remaining_seconds)
        context = {
            'transaction_timeout': int(settings.TP_TRANSACTION_TIMEOUT / 60),
            'uuid': uuid,
            'amount': transaction.amount,
            'requested_form': transaction.merchant_account.merchant_account_name,
            'company_website': transaction.merchant_account.company_website,
            'otp_remaining_seconds': otp_remaining_seconds,
        }
        return render(request, 'third_party_transaction/otp.html', context)


    def get_success_url(self, merchant_account, transaction_reference):
        success_redirect_url = merchant_account.redirect_url if merchant_account.redirect_url else merchant_account.company_website
        return f"{success_redirect_url}?ref={transaction_reference}"

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
                'success_url': self.get_success_url(transaction.merchant_account, transaction.reference)
            }
            return JsonResponse(context, status=200)
        else:
            return JsonResponse({'error': "Invalid OTP"}, status=400)
