from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import MerchantTransactionViewSet, CancelWithdrawalTransaction, RegenerateOTP


urlpatterns = [
    url(r'^init-transaction/withdraw/$',
        MerchantTransactionViewSet.as_view({"post": "init_withdrawal_transaction"}),
        name='init_withdrawal_transaction'
    ),
    url(r'^transaction-status/$',
        MerchantTransactionViewSet.as_view({"post": "transaction-status"}),
        name='transaction-status'
    ),
    url(r'^cancel-withdrawal-transaction/$',
        CancelWithdrawalTransaction.as_view(),
        name='cancel_withdrawal_transaction'
    ),
    url(r'^regenerate-otp/$',
        RegenerateOTP.as_view(),
        name='regenerate_otp'
    ),
]
