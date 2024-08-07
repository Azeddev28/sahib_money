from django.conf import settings
from django.urls import reverse
from rest_framework.permissions import BasePermission
from apps.third_party_transaction.utils import generate_signature
from apps.third_party_transaction.models import MerchantAccount


class IsAuthorizedMerchant(BasePermission):
    """
    permission to verify merchant
    """
    message = 'Merchant not verified'

    def has_permission(self, request, view):
        merchant_app_key = request.POST.get('app_key')
        transaction_reference = request.POST.get('transaction_reference', '')
        transaction_signature = request.POST.get('transaction_signature', '')
        merchant_account = MerchantAccount.objects.get(merchant_app_key=merchant_app_key)
        merchant_secret_key = merchant_account.merchant_secret_key
        signature = generate_signature(transaction_reference, merchant_app_key, merchant_secret_key)
        return signature == transaction_signature
