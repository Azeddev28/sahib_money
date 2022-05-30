from apps.payments.views import DepositPaymentView, WithdrawPaymentView

from django.contrib.auth.decorators import login_required


deposit_payment_view = login_required(DepositPaymentView.as_view())
withdraw_payment_view = login_required(WithdrawPaymentView.as_view())
