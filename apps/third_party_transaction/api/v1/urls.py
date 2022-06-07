from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from .views import TPTransactionViewSet


urlpatterns = [
    url(r'^init_transaction/withdraw/$',
        TPTransactionViewSet.as_view({"post": "init_withdrawal_transaction"}),
        name='init_withdrawal_transaction'
    ),
]
