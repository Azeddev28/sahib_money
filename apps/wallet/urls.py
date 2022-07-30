from django.urls import path

from apps.wallet.bindings import (deposit_transaction_view,
                                  transaction_list_view,
                                  deposit_request_list_view)


urlpatterns = [
    path('deposit/', deposit_transaction_view, name='payment-deposit'),
    path('transactions-list', transaction_list_view, name='transaction-list'),
    path('deposit-requests', deposit_request_list_view, name='deposit-requests'),
]
