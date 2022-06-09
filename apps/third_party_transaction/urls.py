from django.conf import settings
from django.urls import include, path

from apps.third_party_transaction.api.v1 import urls as tp_transaction_api_v1


urlpatterns = [
    path('api/v1/', include(tp_transaction_api_v1)),
]
