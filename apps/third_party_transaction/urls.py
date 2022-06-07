from django.conf import settings
from django.urls import include, path

from apps.third_party_transaction.api.v1 import urls as tp_transaction_api_v1
from apps.third_party_transaction.views import OTPView

urlpatterns = [
    path('api/v1/', include(tp_transaction_api_v1)),
    path('otp/<uuid:uuid>', OTPView.as_view(), name='otp'),
]
