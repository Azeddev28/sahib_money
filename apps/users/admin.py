from django.contrib import admin
from django.contrib.auth import get_user_model
from apps.users.models import MerchantAccount

User = get_user_model()


class MerchantAccountAdmin(admin.ModelAdmin):
    class Meta:
        model = MerchantAccount

    readonly_fields = ['merchant_app_key', 'merchant_secret_key']


admin.site.register(MerchantAccount, MerchantAccountAdmin)
admin.site.register(User)
