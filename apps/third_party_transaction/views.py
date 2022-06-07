from django.shortcuts import render
from django.views import View

from apps.third_party_transaction.models import ThirdPartyTransaction, TransactionOTP


class OTPView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        transaction_uuid = request.GET.get('uuid')
        try:
            transaction = ThirdPartyTransaction.objects.get(uuid=transaction_uuid)
        catch ThirdPartyTransaction.DoesNotExist:
            
        if user != transaction.wallet.user:
            # user ki phir kuss paar do
            pass

        otp = TransactionOTP.objects.create(transaction=transaction)

        # user ko email men bhej do aync task men


    def post(self, request, *args, **kwargs):
        # verify otp
        pass
