from django.forms import ModelForm
from apps.users.models import MerchantAccount

class MerchantAccountForm(ModelForm):
    class Meta:
        model = MerchantAccount
        fields = ['redirect_url']