from django.contrib.auth.views import LogoutView

from apps.authentication.views import VerifyAccount


verify_account_view = VerifyAccount.as_view()
logout_view = LogoutView.as_view()
