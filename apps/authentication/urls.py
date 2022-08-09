from django.urls import path

from apps.authentication.bindings import (verify_account_view,
                                          logout_view, login_view,
                                          merchant_register_view, register_view)


urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path('verify-account/<uuid:uuid>', verify_account_view, name='verify-account'),
    path('merchant-register/', merchant_register_view, name='merchant-registration')
]
