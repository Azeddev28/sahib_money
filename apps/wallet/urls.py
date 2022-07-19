from django.urls import path

from apps.wallet.bindings import deposit_transaction_view, wallet_transaction_view, transaction_list_view


urlpatterns = [
    path('deposit/', deposit_transaction_view, name='payment-deposit'),
    path('wallet-transaction/', wallet_transaction_view, name='wallet-transaction'),
    path('transactions-list', transaction_list_view, name='transaction-list')
]
