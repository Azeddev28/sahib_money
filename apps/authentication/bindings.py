from django.contrib.auth.views import LogoutView
from apps.authentication.decorators import authenticated_redirect

from apps.authentication.views import VerifyAccount, LoginView


verify_account_view = VerifyAccount.as_view()
logout_view = LogoutView.as_view()
login_view = authenticated_redirect(LoginView.as_view())
