from django.urls import path

from apps.wallet.bindings import deposit_transaction_view


urlpatterns = [
    path('deposit/', deposit_transaction_view, name='payment-deposit')
]
