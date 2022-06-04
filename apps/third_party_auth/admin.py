from django.contrib import admin

from apps.third_party_auth.models import MerchantAccount, ThirdPartyTransaction


class MerchantAccountAdmin(admin.ModelAdmin):
    class Meta:
        model = MerchantAccount

    readonly_fields = ['merchant_secret_key', 'account_name']


class ThirdPartyTransactionAdmin(admin.ModelAdmin):
    class Meta:
        model = ThirdPartyTransaction

    readonly_fields = ['merchant_account', 'transaction_type', 'wallet', 'amount']

admin.site.register(MerchantAccount, MerchantAccountAdmin)
admin.site.register(ThirdPartyTransaction, ThirdPartyTransactionAdmin)
