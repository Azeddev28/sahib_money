from django.contrib.auth.decorators import login_required

from apps.wallet.views import DepositTransactionView, TransactionListView, WalletTransactionView


deposit_transaction_view = login_required(DepositTransactionView.as_view())
wallet_transaction_view = login_required(WalletTransactionView.as_view())
transaction_list_view = login_required(TransactionListView.as_view())
