from django.urls import path

from apps.wallet.bindings import (deposit_transaction_view,
                                  transaction_list_view,
                                  deposit_request_list_view,
                                  select_bank_list_view,
                                  withdrawal_transaction_view,
                                  withdraw_request_list_view,
                                  wallet_transfer_view)


urlpatterns = [
    path('deposit/', deposit_transaction_view, name='deposit-transaction'),
    path('withdraw/', withdrawal_transaction_view, name='withdrawal-transaction'),
    path('wallet-transfer/', wallet_transfer_view, name='wallet-transfer'),
    path('transactions-list', transaction_list_view, name='transaction-list'),
    path('deposit-requests', deposit_request_list_view, name='deposit-requests'),
    path('select-bank/', select_bank_list_view, name='select-bank'),
    path('withdraw-requests', withdraw_request_list_view, name='withdraw-requests'),
]
