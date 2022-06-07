from django.urls import path

from apps.authentication.views import login_view, register_user
from apps.authentication.bindings import verify_account_view, logout_view


urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path("logout/", logout_view, name="logout"),
    path('verify-account/<uuid:uuid>', verify_account_view, name='verify-account')
]
