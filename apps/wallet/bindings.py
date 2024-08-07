from django.contrib.auth.decorators import login_required

from apps.wallet.views import (DepositRequestListView,
                                SelectBankListView,
                                DepositTransactionView,
                                TransactionListView,
                                WithdrawalTransactionView,
                                WithdrawRequestListView,
                                P2PTransactionView)


deposit_transaction_view = login_required(DepositTransactionView.as_view())
withdrawal_transaction_view = login_required(WithdrawalTransactionView.as_view())
transaction_list_view = login_required(TransactionListView.as_view())
deposit_request_list_view = login_required(DepositRequestListView.as_view())
select_bank_list_view = login_required(SelectBankListView.as_view())
withdraw_request_list_view = login_required(WithdrawRequestListView.as_view())
wallet_transfer_view = login_required(P2PTransactionView.as_view())
