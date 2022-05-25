from django.urls import path
from .views import deposit_payment


urlpatterns = [
    path('deposit/', deposit_payment, name = "payments" ),
]