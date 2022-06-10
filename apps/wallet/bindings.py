from django.contrib.auth.decorators import login_required

from apps.wallet.views import DepositTransactionView


deposit_transaction_view = login_required(DepositTransactionView.as_view())
