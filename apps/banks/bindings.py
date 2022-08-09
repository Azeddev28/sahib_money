from django.contrib.auth.decorators import login_required

from apps.banks.views import UserBankView


user_bank_view = login_required(UserBankView.as_view())
