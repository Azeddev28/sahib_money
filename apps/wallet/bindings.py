from django.contrib.auth.decorators import login_required

from apps.wallet.views import DepositRequestListView, DepositTransactionView, SelectBankListView, TransactionListView


deposit_transaction_view = login_required(DepositTransactionView.as_view())
transaction_list_view = login_required(TransactionListView.as_view())
deposit_request_list_view = login_required(DepositRequestListView.as_view())
select_bank_list_view = login_required(SelectBankListView.as_view())
