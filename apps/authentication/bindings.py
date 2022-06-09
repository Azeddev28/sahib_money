from django.contrib.auth.views import LogoutView
from apps.authentication.views.merchants import MerchantRegisterView

from apps.authentication.views.users import VerifyAccount, LoginView
from apps.authentication.decorators import authenticated_redirect


verify_account_view = VerifyAccount.as_view()
logout_view = LogoutView.as_view()
merchant_register_view = authenticated_redirect(MerchantRegisterView.as_view())
login_view = authenticated_redirect(LoginView.as_view())
