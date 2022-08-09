from django.urls import path

from apps.banks.bindings import user_bank_view


urlpatterns = [
    path('add-bank-details/', user_bank_view, name='user-bank-details'),
]
