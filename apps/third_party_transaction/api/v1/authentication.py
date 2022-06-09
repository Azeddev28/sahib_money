from django.contrib.auth.models import User
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions

from apps.third_party_transaction.models import MerchantAccount


class MerchantAuthentication(BaseAuthentication):
    def authenticate(self, request):
        app_key = request.POST.get('app_key')
        if not app_key:
            raise exceptions.AuthenticationFailed('Merchant app key not provided')

        try:
            merchant_account = MerchantAccount.objects.get(merchant_app_key=app_key)
        except MerchantAccount.DoesNotExist:
            raise exceptions.AuthenticationFailed('No merchant account associated with this key')

        return (merchant_account.account_user, None)
