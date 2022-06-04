from django.contrib import admin

from apps.wallet.models import *


class BankDetailModelAdmin(admin.ModelAdmin):
    class Meta:
        model = BankDetail

    fields = ['__all__']


class DepositTransactionModelAdmin(admin.ModelAdmin):
    class Meta:
        model = DepositTransaction

    fields = ['__all__']


class P2PTransactionModelAdmin(admin.ModelAdmin):
    class Meta:
        model = P2PTransaction

    fields = ['__all__']


class WithdrawalTransactionModelAdmin(admin.ModelAdmin):
    class Meta:
        model = WithdrawalTransaction

    fields = ['__all__']

admin.site.register(BankDetail, BankDetailModelAdmin)
admin.site.register(DepositTransaction, DepositTransactionModelAdmin)
admin.site.register(P2PTransaction, P2PTransactionModelAdmin)
admin.site.register(WithdrawalTransaction, WithdrawalTransactionModelAdmin)
