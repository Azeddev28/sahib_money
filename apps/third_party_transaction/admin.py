from django.contrib import admin

from apps.third_party_transaction.models import MerchantAccount, ThirdPartyTransaction, TransactionOTP


class MerchantAccountAdmin(admin.ModelAdmin):
    class Meta:
        model = MerchantAccount

    readonly_fields = ['merchant_app_key', 'merchant_secret_key']


class ThirdPartyTransactionAdmin(admin.ModelAdmin):
    class Meta:
        model = ThirdPartyTransaction

    readonly_fields = ['uuid', 'wallet', 'merchant_account', 'type', 'status' , 'amount']

class TransactionOTPAdmin(admin.ModelAdmin):
    class Meta:
        model = TransactionOTP

    readonly_fields = ['transaction', 'otp_code', 'created']

admin.site.register(MerchantAccount, MerchantAccountAdmin)
admin.site.register(ThirdPartyTransaction, ThirdPartyTransactionAdmin)
admin.site.register(TransactionOTP, TransactionOTPAdmin)
