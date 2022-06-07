from django.contrib import admin

from apps.wallet.models import *


class WalletModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Wallet


class BankDetailModelAdmin(admin.ModelAdmin):
    class Meta:
        model = BankDetail

    list_display = ('account_no', 'iban_no', 'account_name')


class DepositTransactionModelAdmin(admin.ModelAdmin):
    class Meta:
        model = DepositTransaction

    readonly_fields = ['wallet', 'receipt']


class P2PTransactionModelAdmin(admin.ModelAdmin):
    class Meta:
        model = P2PTransaction

    readonly_fields = ['wallet', 'amount', 'to_wallet']


class WithdrawalTransactionModelAdmin(admin.ModelAdmin):
    class Meta:
        model = WithdrawalTransaction

    readonly_fields = ['wallet', 'bank_details', 'amount']


admin.site.register(BankDetail, BankDetailModelAdmin)
admin.site.register(DepositTransaction, DepositTransactionModelAdmin)
admin.site.register(P2PTransaction, P2PTransactionModelAdmin)
admin.site.register(WithdrawalTransaction, WithdrawalTransactionModelAdmin)
admin.site.register(Wallet, WalletModelAdmin)
