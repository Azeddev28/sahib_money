from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import MerchantTransactionViewSet, CancelWithdrawalTransaction


urlpatterns = [
    url(r'^init_transaction/withdraw/$',
        MerchantTransactionViewSet.as_view({"post": "init_withdrawal_transaction"}),
        name='init_withdrawal_transaction'
    ),
    url(r'^cancel_withdrawal_transaction/$',
        CancelWithdrawalTransaction.as_view(),
        name='cancel_withdrawal_transaction'
    ),
]
