from django.urls import path

from apps.payments.bindings import deposit_payment_view
from apps.payments.bindings import withdraw_payment_view

urlpatterns = [
    path('deposit/', deposit_payment_view, name = "payments"),
    path('withdraw/', withdraw_payment_view, name = "payments"),
]
