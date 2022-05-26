from apps.payments.views import DepositPaymentView

from django.contrib.auth.decorators import login_required


deposit_payment_view = login_required(DepositPaymentView.as_view())

